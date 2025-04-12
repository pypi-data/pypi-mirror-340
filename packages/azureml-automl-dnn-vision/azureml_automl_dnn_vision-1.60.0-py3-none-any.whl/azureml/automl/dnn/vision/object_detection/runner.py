# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Entry script that is invoked by the driver script from automl."""

import argparse
import os
import time
import torch

from typing import Any, Dict, List, Tuple

from azureml.core.run import Run
from azureml.automl.core.shared.constants import Tasks

from azureml.automl.dnn.vision.common import utils
from azureml.automl.dnn.vision.common.artifacts_utils import (
    load_from_pretrained_checkpoint, load_state_from_latest_checkpoint
)
from azureml.automl.dnn.vision.common.constants import (
    SettingsLiterals, DistributedLiterals,
    DistributedParameters, TrainingLiterals as CommonTrainingLiterals
)
from azureml.automl.dnn.vision.common.trainer.lrschedule import setup_lr_scheduler
from azureml.automl.dnn.vision.common.trainer.optimize import setup_optimizer
from azureml.automl.dnn.vision.object_detection.common.constants import (
    training_settings_defaults, ModelLiterals, ModelParameters,
    DataLoaderParameterLiterals, safe_to_log_settings,
    ModelNames, CriterionNames, TilingLiterals
)
from azureml.automl.dnn.vision.object_detection.writers.score import _score_with_model
from azureml.automl.dnn.vision.object_detection.common.parameters import add_model_agnostic_od_train_parameters
from azureml.automl.dnn.vision.object_detection.common.od_training_state import ODTrainingState
from azureml.automl.dnn.vision.object_detection_yolo import runner as yolo_runner

from azureml.train.automl.runtime._code_generation.utilities import generate_vision_code_and_notebook

from .data import datasets, loaders
from .data.utils import read_aml_dataset, read_file_dataset, setup_dataset_wrappers
from .models import detection
from .models.object_detection_model_wrappers import ObjectDetectionModelFactory
from .models.instance_segmentation_model_wrappers import InstanceSegmentationModelFactory
from .trainer import criterion, train
from .common.object_detection_utils import score_validation_data
from ..common import distributed_utils
from ..common.data_utils import get_labels_files_paths_from_settings, validate_labels_files_paths
from ..common.exceptions import AutoMLVisionValidationException, AutoMLVisionRuntimeUserException
from ..common.logging_utils import get_logger, clean_settings_for_logging
from ..common.parameters import add_task_agnostic_train_parameters
from ..common.system_meter import SystemMeter
from azureml.automl.dnn.vision.common.aml_dataset_base_wrapper import AmlDatasetBaseWrapper
from ..common.sku_validation import validate_gpu_sku

from typing import cast, Optional

azureml_run = Run.get_context()

logger = get_logger(__name__)


@utils._exception_handler
def run(automl_settings: Dict[str, Any], mltable_data_json: Optional[str] = None, **kwargs) -> None:
    """Invoke training by passing settings and write the resulting model.

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dictionary
    :param mltable_data_json: Json containing the uri for train/validation/test datasets.
    :type mltable_data_json: str
    """
    script_start_time = time.time()

    settings, unknown = _parse_argument_settings(automl_settings)

    number_of_epochs = settings.get(CommonTrainingLiterals.NUMBER_OF_EPOCHS, None)
    if number_of_epochs <= 0:
        raise AutoMLVisionValidationException("number_of_epochs in automl settings should be a positive integer.",
                                              has_pii=False)

    # Temporary hack to expose yolo as a model_name setting
    model_name = settings.get(SettingsLiterals.MODEL_NAME, None)
    if model_name == ModelNames.YOLO_V5:
        yolo_runner.run(automl_settings, mltable_data_json)
        return

    utils._top_initialization(settings)

    task_type = settings.get(SettingsLiterals.TASK_TYPE, None)

    if not task_type:
        raise AutoMLVisionValidationException("Task type was not found in automl settings.",
                                              has_pii=False)

    if task_type == Tasks.IMAGE_INSTANCE_SEGMENTATION and \
            settings.get(TilingLiterals.TILE_GRID_SIZE, None) is not None:
        raise AutoMLVisionValidationException("Tiling is not supported for the task {}.".format(task_type),
                                              has_pii=False)

    utils._set_logging_parameters(task_type, settings)

    if unknown:
        logger.info("Got unknown args, will ignore them.")

    logger.info("Final settings (pii free): \n {}".format(clean_settings_for_logging(settings, safe_to_log_settings)))
    logger.info("Settings not logged (might contain pii): \n {}".format(settings.keys() - safe_to_log_settings))

    if mltable_data_json is None:
        validate_labels_files_paths(settings)

    # Get datasets
    dataset_wrapper: AmlDatasetBaseWrapper = cast(AmlDatasetBaseWrapper, datasets.AmlDatasetObjectDetection)
    train_ds, validation_ds = utils.get_tabular_dataset(
        settings=settings, mltable_json=mltable_data_json)

    # Log system metrics, eg GPU memory consumption, to help debug problems with loading pretrained model checkpoint.
    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    # Download required files before launching train_worker to avoid concurrency issues in distributed mode
    if task_type == Tasks.IMAGE_INSTANCE_SEGMENTATION:
        utils.download_or_mount_required_files(settings, train_ds, validation_ds, dataset_wrapper,
                                               InstanceSegmentationModelFactory(), azureml_run.experiment.workspace)
    else:
        utils.download_or_mount_required_files(settings, train_ds, validation_ds, dataset_wrapper,
                                               ObjectDetectionModelFactory(), azureml_run.experiment.workspace)

    utils.launch_training_with_retries(
        settings=settings, train_worker_fn=train_worker,
        additional_train_worker_fn_args=(mltable_data_json,), logger=logger, azureml_run=azureml_run)

    enable_code_generation = settings.get(SettingsLiterals.ENABLE_CODE_GENERATION, True)
    logger.info("Code generation enabled: {}".format(enable_code_generation))
    if enable_code_generation:
        generate_vision_code_and_notebook(azureml_run)

    utils.log_script_duration(script_start_time, settings, azureml_run)


# Adding handler to log exceptions directly in the child process if using multigpu
@utils._exception_logger
def train_worker(local_rank: int, settings: Dict[str, Any], mltable_data_json) -> None:
    """Invoke training on a single device and write the resulting model.

    :param local_rank: Local rank of the process within the node if invoked in distributed mode. 0 otherwise.
    :type local_rank: int
    :param settings: Dictionary with all training and model settings
    :type settings: Dict[str, Any]
    :param mltable_data_json: MLTable json
    :param type: str
    """
    distributed = settings[DistributedLiterals.DISTRIBUTED]
    if distributed:
        distributed_utils.setup_distributed_training(local_rank, settings, logger)

    system_meter = SystemMeter(log_static_sys_info=True)
    system_meter.log_system_stats()

    model_name = settings[SettingsLiterals.MODEL_NAME]
    if distributed:
        settings[SettingsLiterals.DEVICE] = torch.device("cuda:" + str(local_rank))
    device = settings[SettingsLiterals.DEVICE]
    master_process = distributed_utils.master_process()
    validate_free_gpu_mem = False if settings[SettingsLiterals.RESUME_FROM_STATE] else True
    validate_gpu_sku(device=device, validate_free_gpu_mem=validate_free_gpu_mem)

    utils.warn_for_cpu_devices(device, azureml_run)
    utils.set_run_traits(azureml_run, settings)

    # Set dataloaders' num_workers
    num_workers = settings.get(SettingsLiterals.NUM_WORKERS, None)

    train_data_loader_settings = {
        DataLoaderParameterLiterals.BATCH_SIZE: settings[CommonTrainingLiterals.TRAINING_BATCH_SIZE],
        DataLoaderParameterLiterals.SHUFFLE: True,
        DataLoaderParameterLiterals.NUM_WORKERS: num_workers,
        DataLoaderParameterLiterals.DISTRIBUTED: distributed,
        DataLoaderParameterLiterals.DROP_LAST: False}

    validation_data_loader_settings = {
        DataLoaderParameterLiterals.BATCH_SIZE: settings[CommonTrainingLiterals.VALIDATION_BATCH_SIZE],
        DataLoaderParameterLiterals.SHUFFLE: False,
        DataLoaderParameterLiterals.NUM_WORKERS: num_workers,
        DataLoaderParameterLiterals.DISTRIBUTED: distributed,
        DataLoaderParameterLiterals.DROP_LAST: False}

    # Set randomization seed for deterministic training.
    random_seed = settings.get(SettingsLiterals.RANDOM_SEED, None)
    if distributed and random_seed is None:
        # Set by default for distributed training to ensure
        # all workers have same random parameters.
        random_seed = DistributedParameters.DEFAULT_RANDOM_SEED
    utils._set_random_seed(random_seed)
    utils._set_deterministic(settings.get(SettingsLiterals.DETERMINISTIC, False))

    # Extract Automl Settings
    validation_size = settings[CommonTrainingLiterals.VALIDATION_SIZE]
    ignore_data_errors = settings.get(SettingsLiterals.IGNORE_DATA_ERRORS, True)
    output_directory = settings[SettingsLiterals.OUTPUT_DIR]
    run_scoring = settings.get(SettingsLiterals.OUTPUT_SCORING, False)

    task_type = settings.get(SettingsLiterals.TASK_TYPE, None)
    masks_required = task_type == Tasks.IMAGE_INSTANCE_SEGMENTATION

    tile_grid_size = settings.get(TilingLiterals.TILE_GRID_SIZE, None)
    tile_overlap_ratio = settings.get(TilingLiterals.TILE_OVERLAP_RATIO, None)
    label_column_name = settings.get(SettingsLiterals.LABEL_COLUMN_NAME, None)
    # Setup Dataset
    use_bg_label = detection.use_bg_label(model_name)

    # Get datasets
    train_ds, validation_ds = utils.get_tabular_dataset(
        settings=settings, mltable_json=mltable_data_json)

    if train_ds is not None:
        train_dataset_wrapper, valid_dataset_wrapper = read_aml_dataset(dataset=train_ds,
                                                                        validation_dataset=validation_ds,
                                                                        validation_size=validation_size,
                                                                        ignore_data_errors=ignore_data_errors,
                                                                        output_dir=output_directory,
                                                                        master_process=master_process,
                                                                        use_bg_label=use_bg_label,
                                                                        settings=settings,
                                                                        masks_required=masks_required,
                                                                        label_column_name=label_column_name,
                                                                        tile_grid_size=tile_grid_size,
                                                                        tile_overlap_ratio=tile_overlap_ratio)
    else:
        image_folder = settings.get(SettingsLiterals.IMAGE_FOLDER, None)

        if image_folder is None:
            raise AutoMLVisionValidationException("Either images_folder or dataset_id needs to be specified",
                                                  has_pii=False)
        else:
            image_folder = os.path.join(settings[SettingsLiterals.DATA_FOLDER], image_folder)

        annotations_file, annotations_test_file = get_labels_files_paths_from_settings(settings)

        train_dataset_wrapper, valid_dataset_wrapper = read_file_dataset(image_folder=image_folder,
                                                                         annotations_file=annotations_file,
                                                                         annotations_test_file=annotations_test_file,
                                                                         validation_size=validation_size,
                                                                         ignore_data_errors=ignore_data_errors,
                                                                         output_dir=output_directory,
                                                                         master_process=master_process,
                                                                         use_bg_label=use_bg_label,
                                                                         masks_required=masks_required,
                                                                         tile_grid_size=tile_grid_size,
                                                                         tile_overlap_ratio=tile_overlap_ratio)
        logger.info("[train file: {}, validation file: {}]".format(annotations_file, annotations_test_file))

    if train_dataset_wrapper.classes != valid_dataset_wrapper.classes:
        all_classes = list(
            set(train_dataset_wrapper.classes + valid_dataset_wrapper.classes))
        train_dataset_wrapper.reset_classes(all_classes)
        valid_dataset_wrapper.reset_classes(all_classes)

    logger.info("# train images: {}, # validation images: {}, # labels: {}".format(
        len(train_dataset_wrapper), len(valid_dataset_wrapper),
        train_dataset_wrapper.num_classes - 1))  # excluding "--bg--" class

    training_dataset_wrapper, validation_dataset_wrapper = setup_dataset_wrappers(
        train_dataset_wrapper, valid_dataset_wrapper, tile_grid_size)

    # Setup Model
    model_wrapper = detection.setup_model(model_name=model_name,
                                          number_of_classes=training_dataset_wrapper.dataset.num_classes,
                                          classes=training_dataset_wrapper.dataset.classes,
                                          device=device,
                                          distributed=distributed,
                                          local_rank=local_rank,
                                          settings=settings)

    # if the model exposes some transformations
    # enable those in the datasets.
    training_dataset_wrapper.dataset.transform = model_wrapper.get_train_validation_transform()
    validation_dataset_wrapper.dataset.transform = model_wrapper.get_train_validation_transform()
    # Replace model.transform resize and normalize with identity methods
    # so that we avoid re-doing the transform in the model
    if training_dataset_wrapper.dataset.transform is not None and \
            validation_dataset_wrapper.dataset.transform is not None:
        logger.info("Found transform not None in both training and validation dataset - disabling in model.")
        model_wrapper.disable_model_transform()
    else:
        logger.info("Transform is None for datasets. Keep it in the model - this will increase GPU mem usage.")

    # Load model weight from previously saved checkpoint for incremental training
    load_from_pretrained_checkpoint(settings, model_wrapper, distributed)

    num_params = sum([p.data.nelement() for p in model_wrapper.parameters()])
    logger.info("[model: {}, #param: {}]".format(model_name, num_params))

    # Setup Dataloaders

    train_loader = loaders.setup_dataloader(training_dataset_wrapper, **train_data_loader_settings)
    validation_loader = loaders.setup_dataloader(validation_dataset_wrapper, **validation_data_loader_settings)

    # setup optimizer
    optimizer = setup_optimizer(model_wrapper.model, settings=settings)
    # setup lr_scheduler
    lr_scheduler = setup_lr_scheduler(optimizer, batches_per_epoch=len(train_loader), settings=settings)
    loss_function = criterion.setup_criterion(CriterionNames.LOSS_FROM_MODEL)

    # Train Model

    logger.info("[start training: train batch_size: {}, val batch_size: {}]".format(
        train_data_loader_settings[DataLoaderParameterLiterals.BATCH_SIZE],
        validation_data_loader_settings[DataLoaderParameterLiterals.BATCH_SIZE]))

    system_meter.log_system_stats()

    training_state = ODTrainingState()
    resume_from_state = settings[SettingsLiterals.RESUME_FROM_STATE]
    if resume_from_state:
        # Load model, optimizer, scheduler, training state from saved checkpoint
        load_state_from_latest_checkpoint(output_dir=output_directory, run=azureml_run, model_wrapper=model_wrapper,
                                          distributed=distributed, optimizer=optimizer, scheduler=lr_scheduler,
                                          training_state=training_state)

    train.train(model=model_wrapper,
                optimizer=optimizer,
                scheduler=lr_scheduler,
                train_data_loader=train_loader,
                val_data_loader=validation_loader,
                criterion=loss_function,
                device=device,
                settings=settings,
                training_state=training_state,
                output_dir=output_directory,
                azureml_run=azureml_run)

    if master_process and run_scoring:
        score_validation_data(run=azureml_run, model_settings=model_wrapper.model_settings.get_settings_dict(),
                              settings=settings, device=device,
                              val_dataset=validation_ds,
                              score_with_model=_score_with_model)


def _parse_argument_settings(automl_settings: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    """Parse all arguments and merge settings

    :param automl_settings: Dictionary with all training and model settings
    :type automl_settings: Dict[str, Any]
    :return: tuple of the automl settings dictionary with all settings filled in and a list of any unknown args
    :rtype: Tuple[Dict[str, Any], List[str]]
    """

    parser = argparse.ArgumentParser(description="Object detection", allow_abbrev=False, add_help=False)
    add_task_agnostic_train_parameters(parser, training_settings_defaults)
    add_model_agnostic_od_train_parameters(parser, training_settings_defaults)

    # Model Settings
    parser.add_argument(utils._make_arg(ModelLiterals.MIN_SIZE), type=utils._convert_type_to_int,
                        help="Minimum size of the image to be rescaled before feeding it to the backbone",
                        default=ModelParameters.DEFAULT_MIN_SIZE)

    parser.add_argument(utils._make_arg(ModelLiterals.MAX_SIZE), type=utils._convert_type_to_int,
                        help="Maximum size of the image to be rescaled before feeding it to the backbone",
                        default=ModelParameters.DEFAULT_MAX_SIZE)

    parser.add_argument(utils._make_arg(ModelLiterals.BOX_SCORE_THRESH), type=float,
                        help="During inference, only return proposals with a classification score \
                        greater than box_score_thresh",
                        default=ModelParameters.DEFAULT_BOX_SCORE_THRESH)

    parser.add_argument(utils._make_arg(ModelLiterals.NMS_IOU_THRESH), type=float,
                        help="NMS threshold for the prediction head. Used during inference",
                        default=ModelParameters.DEFAULT_NMS_IOU_THRESH)

    parser.add_argument(utils._make_arg(ModelLiterals.BOX_DETECTIONS_PER_IMG), type=utils._convert_type_to_int,
                        help="Maximum number of detections per image, for all classes.",
                        default=ModelParameters.DEFAULT_BOX_DETECTIONS_PER_IMG)

    args, unknown = parser.parse_known_args()
    args_dict = vars(args)
    args_dict, unknown_search_space_args = utils.parse_model_conditional_space(args_dict, parser)
    if unknown_search_space_args:
        logger.info("Got unknown search_space args, will ignore them.")

    utils.set_validation_size(automl_settings, args_dict)
    utils.unpack_advanced_settings(automl_settings)
    merged_dict = utils._merge_settings_args_defaults(automl_settings, args_dict, training_settings_defaults)

    # When tile_grid_size is passed as part of conditional HP space or in automlsettings,
    # it would be a string. This functions parses the string and converts it to a tuple.
    utils.fix_tiling_settings(merged_dict)
    return merged_dict, unknown
