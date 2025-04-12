import pytest
import uuid

from typing import List
from unittest.mock import patch

from azureml.automl.dnn.vision.classification.io.read.dataset_wrappers import ImageFolderDatasetWrapper, \
    ImageFolderLabelFileDatasetWrapper, AmlDatasetWrapper
from azureml.automl.dnn.vision.common.utils import _save_image_df
from azureml.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from azureml.automl.dnn.vision.common.dataset_helper import AmlDatasetHelper

from .aml_dataset_mock import DataflowStreamMock
from ..common.aml_dataset_mock import AmlDatasetMock, DataflowMock
from ..common.run_mock import ClassificationDatasetWrapperMock
import os
import pandas as pd


@pytest.mark.usefixtures('new_clean_dir')
class TestImageFolderDatasetWrapper:
    def test_generate_labels_files_from_imagefolder(self):
        dataset_wrapper = ImageFolderDatasetWrapper(
            'classification_data/image_folder_format')
        assert len(dataset_wrapper) == 4
        # check whether all images are in
        labels = []
        for _, label in dataset_wrapper:
            labels.append(label)

        assert len(set(labels)) == 2
        assert dataset_wrapper.num_classes == 2


@pytest.mark.usefixtures('new_clean_dir')
class TestImageFolderLabelFileDatasetWrapper:
    def test_get_labels(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=True
        )
        assert len(dataset_wrapper) == 4
        labels = []
        for _, label in dataset_wrapper:
            labels.extend(label)

        assert len(set(labels)) == 2

    def test_valid_dataset(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=True
        )

        valid_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/valid_labels.csv',
            all_labels=dataset_wrapper.labels,
            multilabel=True
        )

        assert valid_dataset_wrapper.labels == dataset_wrapper.labels

    def test_labels_with_tabs(self):
        labels_file = str(uuid.uuid4())[:7] + '.txt'
        with open(labels_file, 'w') as fp:
            fp.write('crack_1.jpg\t"label_1\t"')

        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file=labels_file
        )

        assert dataset_wrapper.labels == ['label_1\t']

    def test_labels_with_commas(self):
        labels_file = str(uuid.uuid4())[:7] + '.txt'
        with open(labels_file, 'w') as fp:
            fp.write('"crack_1.jpg"\t\'label_1,label_2\', label_3')

        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file=labels_file,
            multilabel=True
        )

        assert set(dataset_wrapper.labels) == set(['label_1,label_2', 'label_3'])

    def test_missing_labels_in_validation(self):
        dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/binary_classification.csv',
            multilabel=True
        )

        valid_dataset_wrapper = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/invalid_labels.txt',
            all_labels=dataset_wrapper.labels,
            multilabel=True
        )

        assert set(dataset_wrapper.labels).issubset(set(valid_dataset_wrapper.labels))

        dataset_wrapper.reset_labels(valid_dataset_wrapper.labels)

        assert dataset_wrapper.labels == valid_dataset_wrapper.labels

    def test_bad_line_in_input_file(self):
        with pytest.raises(AutoMLVisionDataException):
            ImageFolderLabelFileDatasetWrapper(
                'classification_data/images',
                input_file='classification_data/multiclass_bad_line.csv',
                ignore_data_errors=False
            )

        dataset = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/multiclass_bad_line.csv',
            ignore_data_errors=True
        )

        assert len(dataset) == 3

    def test_missing_images_in_input_file(self):
        with pytest.raises(AutoMLVisionDataException):
            ImageFolderLabelFileDatasetWrapper(
                'classification_data/images',
                input_file='classification_data/multiclass_missing_image.csv',
                ignore_data_errors=False
            )

        dataset = ImageFolderLabelFileDatasetWrapper(
            'classification_data/images',
            input_file='classification_data/multiclass_missing_image.csv',
            ignore_data_errors=True
        )

        assert len(dataset) == 3


@pytest.mark.usefixtures('new_clean_dir')
class TestAmlDatasetDatasetWrapper:

    @staticmethod
    def _build_dataset(properties={},
                       image_column='image_url',
                       label_column='label',
                       number_of_files=2,
                       test_labels=['cat', 'dog'],
                       number_of_files_to_remove=0):
        test_dataset_id = 'd7c014ec-474a-49f4-8ae3-09049c701913'
        test_files = []
        for i in range(number_of_files):
            test_files.append('d7c014ec-474a-49f4-8ae3-09049c701913-{}.txt'.format(i))
        test_files_full_path = [os.path.join(AmlDatasetHelper.get_data_dir(),
                                             test_file) for test_file in test_files]
        label_dataset_data = {
            image_column: test_files,
            label_column: test_labels
        }

        files_subset = test_files_full_path[:len(test_files_full_path) - number_of_files_to_remove]
        labels_subset = test_labels[:len(test_labels) - number_of_files_to_remove]

        dataframe = pd.DataFrame(label_dataset_data)
        mockdataflowstream = DataflowStreamMock(files_subset)
        mockdataflow = DataflowMock(dataframe, image_column, mockdataflowstream)
        mockdataset = AmlDatasetMock(properties, mockdataflow, test_dataset_id)
        return mockdataset, files_subset, labels_subset

    @staticmethod
    def _test_datasetwrapper(dataset, test_files, test_labels,
                             multilabel=False, ignore_data_errors=False, stream_image_files=False):
        try:
            AmlDatasetWrapper.download_image_files(dataset)
            datasetwrapper = AmlDatasetWrapper(dataset, multilabel=multilabel,
                                               ignore_data_errors=ignore_data_errors,
                                               stream_image_files=stream_image_files)

            for i, test_label in enumerate(test_labels):
                assert datasetwrapper.label_at_index(i) == test_label, "Test label {}".format(i)

            labels = datasetwrapper.labels
            # flatten the test labels
            flatten_test_labels = []
            for label in test_labels:
                if isinstance(label, List):
                    flatten_test_labels += label
                else:
                    flatten_test_labels.append(label)
            assert set(flatten_test_labels) == set(labels), "Labels"
            assert datasetwrapper.multilabel == multilabel, "Multilabel"
            assert len(datasetwrapper) == len(test_files), "len"

            for test_file in test_files:
                assert os.path.exists(test_file)

        finally:
            for test_file in test_files:
                os.remove(test_file)

    @pytest.mark.parametrize("stream_image_files", [True, False])
    def test_aml_dataset_wrapper_default(self, stream_image_files):
        mockdataset, test_files, test_labels = self._build_dataset()

        self._test_datasetwrapper(mockdataset, test_files, test_labels, stream_image_files=stream_image_files)

    def test_aml_dataset_wrapper_integer_labels(self):
        test_label0 = 1
        test_label1 = 2
        mockdataset, test_files, test_labels = self._build_dataset(test_labels=[test_label0, test_label1])

        self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=False)

    def test_aml_dataset_wrapper_properties(self):
        image_column = 'f'
        label_column = 'x'
        properties = {'_Image_Column:Image_': {'Column': image_column,
                                               'DetailsColumn': 'image_details'},
                      '_Label_Column:Label_': {'Column': label_column, 'Type': 'Classification'}}

        mockdataset, test_files, test_labels = self._build_dataset(properties,
                                                                   image_column,
                                                                   label_column)

        self._test_datasetwrapper(mockdataset, test_files, test_labels)

    @pytest.mark.parametrize("stream_image_files", [True, False])
    def test_aml_dataset_wrapper_multilabel(self, stream_image_files):
        test_label0 = ['cat', 'white']
        test_label1 = ['dog', 'black']
        mockdataset, test_files, test_labels = self._build_dataset(
            test_labels=[test_label0, test_label1])

        self._test_datasetwrapper(
            mockdataset, test_files, test_labels, multilabel=True, stream_image_files=stream_image_files)

    def test_aml_dataset_wrapper_with_some_multiclass_data(self):
        test_labels = [['cat', 'white'], 'horse', ['dog', 'black']]
        mockdataset, test_files, test_labels = self._build_dataset(number_of_files=3,
                                                                   test_labels=test_labels)

        # Item at index 1 should be removed by the dataset init.
        test_files = [file for index, file in enumerate(test_files) if index != 1]
        test_labels = [label for index, label in enumerate(test_labels) if index != 1]

        self._test_datasetwrapper(mockdataset, test_files, test_labels,
                                  ignore_data_errors=True, multilabel=True)

    def test_aml_dataset_wrapper_multilabel_with_multiclass_dataset(self):
        EXCEPTION_MSG = "Label should be a list of strings or integers for multilabel. " \
            "Found some datapoints with single label or label of other type than str/int. "
        mockdataset, test_files, test_labels = self._build_dataset()

        # When label is string and not list
        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=False, multilabel=True)

        # Note: must e.value.message because pytest's ExceptionInfo sometimes abbreviates the message.
        assert EXCEPTION_MSG in e.value.message

        # When label is list, but has elements that are not str
        test_label0 = [{}, {}]
        test_label1 = ['dog', 'black']
        mockdataset, test_files, test_labels = self._build_dataset(test_labels=[test_label0, test_label1])

        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=False, multilabel=True)

        assert EXCEPTION_MSG in e.value.message

    def test_aml_dataset_wrapper_multilabel_with_multiclass_dataset_ignore_data_errors(self):
        mockdataset, test_files, test_labels = self._build_dataset()

        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=True, multilabel=True)

        assert "No valid datapoints found to initialize dataset." in str(e)

    def test_aml_dataset_wrapper_multiclass_with_multilabel_dataset(self):
        test_label0 = ['cat', 'white']
        test_label1 = ['dog', 'black']
        mockdataset, test_files, test_labels = self._build_dataset(test_labels=[test_label0, test_label1])

        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=False)

        assert "Label should be a string or integer for multiclass. " \
            "Found some datapoints with label of other type than str/int. " in e.value.message

    def test_aml_dataset_wrapper_multiclass_with_multilabel_dataset_ignore_data_errors(self):
        test_label0 = ['cat', 'white']
        test_label1 = ['dog', 'black']
        mockdataset, test_files, test_labels = self._build_dataset(test_labels=[test_label0, test_label1])

        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=True)

        assert "No valid datapoints found to initialize dataset." in str(e)

    def test_aml_dataset_wrapper_multiclass_with_object_detection_dataset(self):
        test_label0 = {'label': 'cat', 'topX': 0.2, 'topY': 0.25, 'bottomX': 0.46, 'bottomY': 0.78, 'isCrowd': 0}
        test_label1 = {'label': 'dog', 'topX': 0.28, 'topY': 0.39, 'bottomX': 0.63, 'bottomY': 0.64, 'isCrowd': 0}
        mockdataset, test_files, test_labels = self._build_dataset(test_labels=[test_label0, test_label1])

        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=False)

        assert "Label should be a string or integer for multiclass. " \
            "Found some datapoints with label of other type than str/int. " in e.value.message

    def test_aml_dataset_wrapper_multiclass_with_mixed_dataset(self):
        test_label0 = 'horse'
        test_label1 = ['cat', 'white']
        test_label2 = {'label': 'dog', 'topX': 0.28, 'topY': 0.39, 'bottomX': 0.63, 'bottomY': 0.64, 'isCrowd': 0}
        mockdataset, test_files, test_labels = self._build_dataset(
            number_of_files=3, test_labels=[test_label0, test_label1, test_label2]
        )

        with pytest.raises(AutoMLVisionDataException) as e:
            self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=False)

        assert "Label should be a string or integer for multiclass. " \
            "Found some datapoints with label of other type than str/int. " in e.value.message

    def test_aml_dataset_wrapper_ignore_missing(self):
        mockdataset, test_files, test_labels = \
            self._build_dataset(number_of_files_to_remove=1)

        self._test_datasetwrapper(mockdataset, test_files, test_labels, ignore_data_errors=True)

    def test_aml_dataset_wrapper_train_test_split(self):
        mockdataset, test_files, test_labels = self._build_dataset()

        try:
            AmlDatasetWrapper.download_image_files(mockdataset)
            datasetwrapper = AmlDatasetWrapper(mockdataset)
            train_dataset_wrapper, valid_dataset_wrapper = datasetwrapper.train_val_split()
            _save_image_df(train_df=train_dataset_wrapper._images_df, val_df=valid_dataset_wrapper._images_df,
                           output_dir='.')

            if train_dataset_wrapper.labels != valid_dataset_wrapper.labels:
                all_labels = list(set(train_dataset_wrapper.labels + valid_dataset_wrapper.labels))
                train_dataset_wrapper.reset_labels(all_labels)
                valid_dataset_wrapper.reset_labels(all_labels)

            num_train_files = len(train_dataset_wrapper._CommonImageDatasetWrapper__files)
            num_valid_files = len(valid_dataset_wrapper._CommonImageDatasetWrapper__files)
            assert len(datasetwrapper._CommonImageDatasetWrapper__files) == num_train_files + num_valid_files
            assert sorted(datasetwrapper.labels) == sorted(all_labels)

            for test_file in test_files:
                assert os.path.exists(test_file)
            # it's train_df.csv and val_df.csv files created from _save_image_df function
            assert os.path.exists('train_df.csv')
            assert os.path.exists('val_df.csv')
        finally:
            for test_file in test_files:
                os.remove(test_file)
            os.remove('train_df.csv')
            os.remove('val_df.csv')

    def test_reset_labels(self):
        num_classes = 3
        labels = ["label_{}".format(i) for i in range(num_classes)]
        datasetwrapper = ClassificationDatasetWrapperMock([7, 7, 7, 7], num_classes)
        datasetwrapper.reset_labels(labels)

        assert datasetwrapper.labels == labels
        assert list(datasetwrapper.label_freq_dict.keys()) == labels

        del datasetwrapper.label_freq_dict['label_2']
        # when len(label_freq_dict) < len(labels), reset_labels should add 'label2' in label_freq_dict with count zero.
        assert len(list(datasetwrapper.label_freq_dict.keys())) == 2
        datasetwrapper.reset_labels(labels)
        assert len(list(datasetwrapper.label_freq_dict.keys())) == 3
        assert datasetwrapper.label_freq_dict['label_2'] == 0
        assert list(datasetwrapper.label_freq_dict.keys()) == labels

        datasetwrapper.label_freq_dict.update({'label_4': 3})
        # when len(label_freq_dict) > len(labels), reset_labels should add additional labels in "labels" list.
        datasetwrapper.reset_labels(labels)
        assert list(datasetwrapper.label_freq_dict.keys()) == labels + ['label_4']
        assert datasetwrapper.labels == labels + ['label_4']

        for key in datasetwrapper.label_freq_dict:
            assert key in datasetwrapper.label_to_index_map

    @patch('os.path.exists')
    def test_aml_dataset_wrapper_streaming_image_files(self, mock_os_path_exists):
        dataset, image_file_paths, _ = self._build_dataset()

        image_file_paths_checked_for_existence = False

        def mock_os_path_exists_side_effect(path):
            nonlocal image_file_paths_checked_for_existence
            for image_file_path in image_file_paths:
                if os.path.normpath(image_file_path) == os.path.normpath(path):
                    image_file_paths_checked_for_existence = True
                    break
            return True
        mock_os_path_exists.side_effect = mock_os_path_exists_side_effect

        AmlDatasetWrapper(dataset, ignore_data_errors=True, stream_image_files=True)
        assert not image_file_paths_checked_for_existence

        image_file_paths_checked_for_existence = False
        AmlDatasetWrapper(dataset, ignore_data_errors=False, stream_image_files=True)
        assert not image_file_paths_checked_for_existence

        image_file_paths_checked_for_existence = False
        AmlDatasetWrapper(dataset, ignore_data_errors=True, stream_image_files=False)
        assert image_file_paths_checked_for_existence

        image_file_paths_checked_for_existence = False
        AmlDatasetWrapper(dataset, ignore_data_errors=False, stream_image_files=False)
        assert image_file_paths_checked_for_existence


if __name__ == "__main__":
    pytest.main([__file__])
