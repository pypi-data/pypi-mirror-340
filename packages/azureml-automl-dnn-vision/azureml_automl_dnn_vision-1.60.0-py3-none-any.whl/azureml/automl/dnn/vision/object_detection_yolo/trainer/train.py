# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

""" Contain functions for training and validation """

import copy
import gc
import math
import sys
import os
import random
import time
import torch
from typing import Any, Dict

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import InsufficientGPUMemory
from azureml.automl.dnn.vision.common import utils, distributed_utils
from azureml.automl.dnn.vision.common.artifacts_utils import save_model_checkpoint, write_artifacts, \
    upload_model_checkpoint
from azureml.automl.dnn.vision.common.average_meter import AverageMeter
from azureml.automl.dnn.vision.common.constants import SettingsLiterals as CommonSettingsLiterals, \
    TrainingLiterals as CommonTrainingLiterals, LogParamsType
from azureml.automl.dnn.vision.common.logging_utils import get_logger
from azureml.automl.dnn.vision.common.system_meter import SystemMeter
from azureml.automl.dnn.vision.common.trainer.lrschedule import LRSchedulerUpdateType
from azureml.automl.dnn.vision.common.exceptions import AutoMLVisionSystemException, AutoMLVisionRuntimeUserException
from azureml.automl.dnn.vision.object_detection.common.constants import ValidationMetricType, TrainingLiterals
from azureml.automl.dnn.vision.object_detection.common.object_detection_utils import compute_metrics, \
    write_per_label_metrics_file
from azureml.automl.dnn.vision.object_detection.data.dataset_wrappers import DatasetProcessingType
from azureml.automl.dnn.vision.object_detection_yolo.eval.yolo_evaluator import YoloEvaluator
from azureml.automl.dnn.vision.object_detection.writers.score_script_utils import write_scoring_script
from azureml.automl.dnn.vision.object_detection_yolo.common.constants import YoloLiterals
from azureml.automl.dnn.vision.object_detection_yolo.utils.ema import ModelEMA
from azureml.automl.dnn.vision.object_detection_yolo.utils.utils import compute_loss, non_max_suppression
from azureml.automl.runtime.shared.score import constants as scoring_constants
from contextlib import nullcontext

logger = get_logger(__name__)


def train_one_epoch(model, ema, optimizer, scheduler, train_loader,
                    epoch, device, system_meter, grad_accum_steps, grad_clip_type: str,
                    evaluator: YoloEvaluator, print_freq=100, tb_writer=None, distributed=False,
                    ):
    """Train a model for one epoch

    :param model: Model to train
    :type model: <class 'azureml.automl.dnn.vision.object_detection_yolo.models.yolo.Model'>
    :param ema: Model Exponential Moving Average
    :type ema: <class 'azureml.automl.dnn.vision.object_detection_yolo.utils.torch_utils.ModelEMA'>
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_loader: Data loader for training data
    :type train_loader: Pytorch data loader
    :param epoch: Current training epoch
    :type epoch: int
    :param device: Target device
    :type device: Pytorch device
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    :param grad_accum_steps: gradient accumulation steps which is used to accumulate the gradients of those steps
     without updating model variables/weights
    :type grad_accum_steps: int
    :param clip_type: The type of gradient clipping. See GradClipType
    :type grad_clip_type: str
    :param evaluator: evaluation helper
    :type evalator: YoloEvaluator
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param tb_writer: Tensorboard writer
    :type tb_writer: <class 'torch.utils.tensorboard.writer.SummaryWriter'>
    :param distributed: Training in distributed mode or not
    :type distributed: bool
    :returns: mean losses for tensorboard writer
    :rtype: <class 'torch.Tensor'>
    """

    batch_time = AverageMeter()
    data_time = AverageMeter()
    losses = AverageMeter()

    nb = len(train_loader)
    mloss = torch.zeros(4, device='cpu')  # mean losses (lbox, lobj, lcls, loss)

    model.train()

    # grad_accum_steps should be positive, smaller or equal than the number of batches per epoch
    grad_accum_steps = min(len(train_loader), max(grad_accum_steps, 1))
    logger.info("[grad_accumulation_step: {}]".format(grad_accum_steps))
    optimizer.zero_grad()

    end = time.time()
    uneven_batches_context_manager = model.join() if distributed else nullcontext()

    with uneven_batches_context_manager:
        for i, (imgs, targets, infos) in enumerate(utils._data_exception_safe_iterator(iter(train_loader))):
            try:
                # measure data loading time
                data_time.update(time.time() - end)

                ni = i + nb * epoch  # number integrated batches (since train start)
                imgs = imgs.to(device).float() / 255.0  # uint8 to float32, 0 - 255 to 0.0 - 1.0

                # to access model specific parameters from DistributedDataPararrel Object
                hyp = model.module.hyp if distributed else model.hyp
                # Multi scale : need more CUDA memory for bigger image size
                if hyp[YoloLiterals.MULTI_SCALE]:
                    imgsz = hyp[YoloLiterals.IMG_SIZE]
                    gs = hyp['gs']
                    sz = random.randrange(imgsz * 0.5, imgsz * 1.5 + gs) // gs * gs
                    sf = sz / max(imgs.shape[2:])
                    if sf != 1:
                        ns = [math.ceil(x * sf / gs) * gs for x in imgs.shape[2:]]  # new shape (stretched to
                        # gs-multiple)
                        imgs = torch.nn.functional.interpolate(imgs, size=ns, mode='bilinear', align_corners=False)
                    logger.info("{} is enabled".format(YoloLiterals.MULTI_SCALE))

                # Forward
                pred = model(imgs)

                # Loss
                loss, loss_items = compute_loss(pred, targets.to(device), model)
                loss_items = loss_items.to('cpu')
                loss /= grad_accum_steps
                loss_items /= grad_accum_steps

                # raise an UserException if loss is too big
                utils.check_loss_explosion(loss.item())
                loss.backward()

                # evaluate metics on this batch if enabled is set.
                if evaluator.enabled:
                    model.eval()
                    with torch.no_grad():
                        inf_out, pred = model(imgs)
                        inf_out = inf_out.detach()

                        all_targets = targets.detach().cpu().numpy()
                        targets_per_image = [all_targets[all_targets[:, 0] == i, :] for i in range(len(infos))]

                        # Run NMS
                        predictions_per_image = non_max_suppression(inf_out, evaluator.conf_thres,
                                                                    evaluator.nms_iou_threshold,
                                                                    multi_label=False)
                        evaluator.evaluate_predictions(predictions_per_image, infos, targets_per_image)
                    model.train()

                if (i + 1) % grad_accum_steps == 0 or i == len(train_loader) - 1:
                    # gradient clipping
                    utils.clip_gradient(model.parameters(), grad_clip_type)
                    optimizer.step()
                    optimizer.zero_grad()
                    ema.update(model)

            except RuntimeError as runtime_ex:
                if "CUDA out of memory" in str(runtime_ex):
                    azureml_error = AzureMLError.create(InsufficientGPUMemory)
                    raise AutoMLVisionRuntimeUserException._with_error(azureml_error).with_traceback(sys.exc_info()[2])
                raise runtime_ex

            if scheduler.update_type == LRSchedulerUpdateType.BATCH:
                scheduler.lr_scheduler.step()

            # Tensorboard
            if tb_writer:
                tb_writer.add_scalar('lr', scheduler.lr_scheduler.get_last_lr()[0], ni)

            # record loss and measure elapsed time
            losses.update(loss.item(), len(imgs))
            mloss = (mloss * i + loss_items) / (i + 1)  # update mean losses
            batch_time.update(time.time() - end)
            end = time.time()

            # delete tensors which have a valid grad_fn
            del loss, pred

            if i % print_freq == 0 or i == nb - 1:
                mesg = "Epoch: [{0}][{1}/{2}]\t" "lr: {3:.5f}\t" "Time {batch_time.value:.4f}" \
                    "({batch_time.avg:.4f})\t" "Data {data_time.value:.4f}" \
                    "({data_time.avg:.4f})\t" "Loss {loss.value:.4f} " \
                    "({loss.avg:.4f})".format(epoch, i, nb, optimizer.param_groups[0]["lr"],
                                              batch_time=batch_time, data_time=data_time, loss=losses)
                logger.info(mesg)

                system_meter.log_system_stats()

    if scheduler.update_type == LRSchedulerUpdateType.EPOCH:
        scheduler.lr_scheduler.step()

    evaluator.finalize_evaluation()
    return mloss, losses.avg


def validate(
    model, validation_loader, device, system_meter, evaluator: YoloEvaluator, print_freq=100, distributed=False
):
    """Gets model results on validation set.

    :param model: Model to score
    :type model: Pytorch nn.Module
    :param validation_loader: Data loader for validation data
    :type validation_loader: Pytorch Data Loader
    :param device: Target device
    :type device: Pytorch device
    :param system_meter: A SystemMeter to collect system properties
    :type system_meter: SystemMeter
    :param evaluator: Evaluation helper
    :type evalator: YoloEvaluator
    :param print_freq: How often you want to print the output
    :type print_freq: int
    :param distributed: Training in distributed mode or not
    :type distributed: bool
    :returns: List of detections and avg_loss
    :rtype: List of ImageBoxes (see object_detection.common.boundingbox) and a float
    """

    batch_time = AverageMeter()
    losses = AverageMeter()

    nb = len(validation_loader)

    model.eval()
    # We have observed that pytorch DDP does some AllReduce calls during eval model as well.
    # When there are uneven number of batches across worker processes, there is issue with mismatch
    # of distributed calls between processes and it leads to blocked processes and hangs.
    # Using the pytorch model instead of DDP model to run validation to avoid sync calls during eval.
    # One other observation is that AllReduce calls from DDP are only seen when we use .join() during
    # training phase.
    base_torch_model = model.module if distributed else model

    end = time.time()
    for i, (images, all_targets, image_infos) in enumerate(
        utils._data_exception_safe_iterator(iter(validation_loader))
    ):

        # Convert targets to list of NumPy arrays, one per image.
        images = images.to(device).float() / 255.0

        with torch.no_grad():
            # Compute model predictions for the current batch of images.
            inf_out, pred = base_torch_model(images)
            inf_out = inf_out.detach()

            loss, loss_items = compute_loss(pred, all_targets.to(device), model)

            all_targets = all_targets.detach().cpu().numpy()
            targets_per_image = [all_targets[all_targets[:, 0] == i, :] for i in range(len(image_infos))]

            # TODO: expose multi_label as arg to enable multi labels per box
            # Run NMS
            predictions_per_image = non_max_suppression(inf_out, evaluator.conf_thres,
                                                        evaluator.nms_iou_threshold, multi_label=False)

            evaluator.evaluate_predictions(predictions_per_image, image_infos, targets_per_image)

        losses.update(loss.item(), len(images))
        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0 or i == nb - 1:
            mesg = "Test: [{0}/{1}]\t" \
                   "Time {batch_time.value:.4f} ({batch_time.avg:.4f})".format(i, nb,
                                                                               batch_time=batch_time)
            logger.info(mesg)

            system_meter.log_system_stats()

    evaluator.finalize_evaluation()

    return losses.avg


def train(model_wrapper, optimizer, scheduler, train_loader, validation_loader,
          training_state, output_dir=None, azureml_run=None, tb_writer=None):
    """Train a model

    :param model_wrapper: Model to train
    :type model_wrapper: BaseObjectDetectionModelWrapper
    :param optimizer: Optimizer used in training
    :type optimizer: Pytorch optimizer
    :param scheduler: Learning Rate Scheduler wrapper
    :type scheduler: BaseLRSchedulerWrapper (see common.trainer.lrschedule)
    :param train_loader: Data loader with training data
    :type train_loader: Pytorch data loader
    :param validation_loader: Data loader with validation data
    :type validation_loader: Pytorch data loader
    :param training_state: Training state
    :type training_state: ODTrainingState
    :param output_dir: Output directory to write checkpoints to
    :type output_dir: str
     :param azureml_run: azureml run object
    :type azureml_run: azureml.core.run.Run
    :param tb_writer: Tensorboard writer
    :type tb_writer: <class 'torch.utils.tensorboard.writer.SummaryWriter'>
    """

    epoch_time = AverageMeter()

    # Extract relevant parameters from training settings
    settings = model_wrapper.specs
    task_type = settings[CommonSettingsLiterals.TASK_TYPE]
    val_index_map = model_wrapper.classes
    val_metric_type = settings[TrainingLiterals.VALIDATION_METRIC_TYPE]
    number_of_epochs = settings[CommonTrainingLiterals.NUMBER_OF_EPOCHS]
    enable_onnx_norm = settings[CommonSettingsLiterals.ENABLE_ONNX_NORMALIZATION]
    log_verbose_metrics = settings.get(CommonSettingsLiterals.LOG_VERBOSE_METRICS, False)
    log_training_metrics = settings.get(CommonSettingsLiterals.LOG_TRAINING_METRICS,
                                        LogParamsType.DISABLE) == LogParamsType.ENABLE
    log_validation_loss = settings.get(CommonSettingsLiterals.LOG_VALIDATION_LOSS,
                                       LogParamsType.ENABLE) == LogParamsType.ENABLE
    is_enabled_early_stopping = settings[CommonTrainingLiterals.EARLY_STOPPING]
    early_stopping_patience = settings[CommonTrainingLiterals.EARLY_STOPPING_PATIENCE]
    early_stopping_delay = settings[CommonTrainingLiterals.EARLY_STOPPING_DELAY]
    eval_freq = settings[CommonTrainingLiterals.EVALUATION_FREQUENCY]
    checkpoint_freq = settings.get(CommonTrainingLiterals.CHECKPOINT_FREQUENCY, None)
    grad_accum_steps = settings[CommonTrainingLiterals.GRAD_ACCUMULATION_STEP]
    grad_clip_type = settings[CommonTrainingLiterals.GRAD_CLIP_TYPE]
    save_as_mlflow = settings[CommonSettingsLiterals.SAVE_MLFLOW]

    training_dataset_processing_type = train_loader.dataset.dataset_processing_type
    if log_training_metrics and training_dataset_processing_type == DatasetProcessingType.IMAGES_AND_TILES:
        log_training_metrics = False
        logger.warning("Training Metrics won't be computed when \
                        small object detection is enabled by setting tile_grid_size parameter")

    model = model_wrapper.model
    # Exponential moving average
    ema = ModelEMA(model, updates=training_state.ema_updates)

    base_model = model

    distributed = distributed_utils.dist_available_and_initialized()
    master_process = distributed_utils.master_process()

    device = model_wrapper.device

    ema_torch_model = ema.ema.module if distributed else ema.ema
    best_model_wts = training_state.best_model_wts if training_state.best_model_wts is not None else \
        copy.deepcopy(ema_torch_model.state_dict())
    best_score = training_state.best_score
    best_epoch = training_state.best_epoch
    no_progress_counter = training_state.no_progress_counter
    best_model_metrics = training_state.best_model_metrics

    computed_metrics = copy.deepcopy(training_state.computed_metrics)
    per_label_metrics = copy.deepcopy(training_state.per_label_metrics)

    val_index_map = model_wrapper.classes

    epoch_end = time.time()
    train_start = time.time()
    train_sys_meter = SystemMeter()
    valid_sys_meter = SystemMeter()

    # Initialize the evaluators for the training and validation subsets.
    train_evaluator = YoloEvaluator(settings=settings, class_names=val_index_map,
                                    dataset_processing_type=train_loader.dataset.dataset_processing_type,
                                    dataset_wrapper=train_loader.dataset)
    validation_evaluator = YoloEvaluator(settings=settings, class_names=val_index_map,
                                         dataset_processing_type=validation_loader.dataset.dataset_processing_type,
                                         dataset_wrapper=validation_loader.dataset)
    specs = {
        'model_specs': model_wrapper.specs,
        'model_settings': model_wrapper.model_settings.get_settings_dict(),
        'classes': model_wrapper.classes,
        'inference_settings': model_wrapper.inference_settings
    }

    start_epoch = training_state.get_start_epoch(number_of_epochs)
    for epoch in range(start_epoch, number_of_epochs):
        logger.info("Training epoch {}.".format(epoch))

        if distributed:
            if train_loader.distributed_sampler is None:
                msg = "train_data_loader.distributed_sampler is None in distributed mode. " \
                      "Cannot shuffle data after each epoch."
                logger.error(msg)
                raise AutoMLVisionSystemException(msg, has_pii=False)
            train_loader.distributed_sampler.set_epoch(epoch)

        enable_evaluation = log_training_metrics and epoch % eval_freq == 0 and \
            val_metric_type != ValidationMetricType.NONE
        train_evaluator.start_evaluation(enable_evaluation)

        mloss, avg_loss = \
            train_one_epoch(base_model, ema, optimizer, scheduler, train_loader, epoch, device,
                            system_meter=train_sys_meter, grad_accum_steps=grad_accum_steps,
                            grad_clip_type=grad_clip_type, tb_writer=tb_writer, distributed=distributed,
                            evaluator=train_evaluator)

        computed_metrics[scoring_constants.LOG_LOSS + "_train"] = avg_loss
        if train_evaluator.enabled:
            incremental_voc_evaluator = train_evaluator.incremental_voc_evaluator\
                if train_evaluator.eval_voc else None
            compute_metrics(train_evaluator.eval_bounding_boxes,
                            train_evaluator.val_metric_type,
                            train_evaluator.coco_index, incremental_voc_evaluator,
                            computed_metrics, per_label_metrics,
                            train_evaluator.coco_metric_time, train_evaluator.voc_metric_time,
                            train_evaluator.primary_metric, is_train=True)

        ema.update_attr(model)

        # Tensorboard
        if tb_writer and master_process:
            tags = ['train/giou_loss', 'train/obj_loss', 'train/cls_loss']
            for x, tag in zip(list(mloss[:-1]), tags):
                tb_writer.add_scalar(tag, x, epoch)

        map_score = 0.0
        final_epoch = epoch + 1 == number_of_epochs
        if epoch % eval_freq == 0 or final_epoch:
            is_best = False
            if val_metric_type != ValidationMetricType.NONE:
                validation_evaluator.start_evaluation(enable=True)
                avg_loss = \
                    validate(model=model_wrapper.model, validation_loader=validation_loader,
                             device=device, system_meter=valid_sys_meter, distributed=distributed,
                             evaluator=validation_evaluator
                             )

                if log_validation_loss:
                    computed_metrics[scoring_constants.LOG_LOSS] = avg_loss
                incremental_voc_evaluator = validation_evaluator.incremental_voc_evaluator\
                    if validation_evaluator.eval_voc else None
                map_score = compute_metrics(validation_evaluator.eval_bounding_boxes,
                                            validation_evaluator.val_metric_type,
                                            validation_evaluator.coco_index,
                                            incremental_voc_evaluator,
                                            computed_metrics, per_label_metrics,
                                            validation_evaluator.coco_metric_time,
                                            validation_evaluator.voc_metric_time,
                                            validation_evaluator.primary_metric, is_train=False)

                # Tensorboard
                if tb_writer:
                    tb_writer.add_scalar("metrics/mAP_0.5", map_score, epoch)

                # start incrementing no progress counter only after early_stopping_delay
                if epoch >= early_stopping_delay:
                    no_progress_counter += 1

                if map_score > best_score:
                    no_progress_counter = 0

                if map_score >= best_score:
                    is_best = True
                    best_epoch = epoch
                    best_score = map_score
                    best_model_metrics = copy.deepcopy(computed_metrics)
            else:
                logger.info("val_metric_type is None. Not computing metrics.")
                is_best = True
                best_epoch = epoch

            # save best model checkpoint
            if is_best and master_process:
                best_model_wts = copy.deepcopy(ema_torch_model.state_dict())
                save_model_checkpoint(epoch=best_epoch,
                                      model_name=model_wrapper.model_name,
                                      number_of_classes=model_wrapper.number_of_classes,
                                      specs=specs,
                                      model_state=best_model_wts,
                                      optimizer_state=optimizer.state_dict(),
                                      lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                      score=best_score,
                                      metrics=best_model_metrics,
                                      output_dir=output_dir)

            logger.info("Current best primary metric score: {0:.3f} (at epoch {1})".format(round(best_score, 5),
                                                                                           best_epoch))

        # for logging the per_label_metrics
        stop_early = is_enabled_early_stopping and no_progress_counter > early_stopping_patience

        # log to Run History every epoch with previously computed metrics, if not computed in the current epoch
        # to sync the metrics reported index with actual training epoch.
        if master_process and azureml_run is not None:
            utils.log_all_metrics(computed_metrics, azureml_run=azureml_run, add_to_logger=True)

            parent_run = utils.should_log_metrics_to_parent(azureml_run)
            if parent_run:
                utils.log_all_metrics(computed_metrics, azureml_run=parent_run, add_to_logger=True)

            if (final_epoch or stop_early) and best_model_metrics:
                utils.log_detailed_object_detection_metrics(best_model_metrics, azureml_run, val_index_map)

                # If parent is a pipeline run, log all training metrics to parent pipeline as well.
                if parent_run:
                    utils.log_detailed_object_detection_metrics(best_model_metrics, parent_run, val_index_map)

        # measure elapsed time
        epoch_time.update(time.time() - epoch_end)
        epoch_end = time.time()
        mesg = "Epoch-level: [{0}]\t" \
               "Epoch-level Time {epoch_time.value:.4f} ({epoch_time.avg:.4f})".format(epoch, epoch_time=epoch_time)
        logger.info(mesg)

        # save model checkpoint
        if checkpoint_freq is not None and epoch % checkpoint_freq == 0 and master_process:
            training_state.no_progress_counter = no_progress_counter
            training_state.stop_early = stop_early
            training_state.computed_metrics = copy.deepcopy(computed_metrics)
            training_state.per_label_metrics = copy.deepcopy(per_label_metrics)
            training_state.ema_updates = ema.updates
            model_location = save_model_checkpoint(epoch=epoch,
                                                   model_name=model_wrapper.model_name,
                                                   number_of_classes=model_wrapper.number_of_classes,
                                                   specs=specs,
                                                   model_state=copy.deepcopy(ema_torch_model.state_dict()),
                                                   optimizer_state=optimizer.state_dict(),
                                                   lr_scheduler_state=scheduler.lr_scheduler.state_dict(),
                                                   score=map_score,
                                                   metrics=computed_metrics,
                                                   output_dir=output_dir,
                                                   model_file_name_prefix=str(epoch) + '_',
                                                   training_state=training_state)

            upload_model_checkpoint(run=azureml_run, model_location=model_location)

        if stop_early:
            logger.info("No progress registered after {0} epochs. "
                        "Early stopping the run.".format(no_progress_counter))
            break

        # collect garbage after each epoch
        gc.collect()

    # measure total training time
    train_time = time.time() - train_start
    utils.log_end_training_stats(train_time, epoch_time, train_sys_meter, valid_sys_meter)

    if log_verbose_metrics:
        utils.log_verbose_metrics_to_rh(train_time, epoch_time, train_sys_meter, valid_sys_meter, azureml_run)

    current_dir = os.path.dirname(os.path.abspath(__file__))
    score_script_dir = os.path.join(os.path.dirname(current_dir), 'writers')

    if master_process:
        write_scoring_script(output_dir=output_dir,
                             score_script_dir=score_script_dir,
                             task_type=task_type)

        write_per_label_metrics_file(output_dir, per_label_metrics, val_index_map)

        # this is to make sure the layers in ema can be loaded in the model wrapper
        # without it, the names are different (i.e. "model.0.conv.conv.weight" vs "0.conv.conv.weight")
        best_model_weights = {'model.' + k: v for k, v in best_model_wts.items()}

        write_artifacts(model_wrapper=model_wrapper,
                        best_model_weights=best_model_weights,
                        labels=model_wrapper.classes,
                        output_dir=output_dir,
                        run=azureml_run,
                        best_metric=best_score,
                        task_type=task_type,
                        device=device,
                        enable_onnx_norm=enable_onnx_norm,
                        model_settings=model_wrapper.model_settings.get_settings_dict(),
                        save_as_mlflow=save_as_mlflow,
                        is_yolo=True)
