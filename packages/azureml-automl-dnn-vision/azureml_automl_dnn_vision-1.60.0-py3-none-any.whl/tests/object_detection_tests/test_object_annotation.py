import copy
import pytest
import re

from azureml.automl.dnn.vision.common.exceptions import AutoMLVisionDataException
from azureml.automl.dnn.vision.object_detection.common.constants import DatasetFieldLabels
from azureml.automl.dnn.vision.object_detection.data.object_annotation import ObjectAnnotation


def _get_pixel_bbox(normalized_bbox, height, width):
    result = copy.deepcopy(normalized_bbox)
    result[::2] = [x * width for x in result[::2]]
    result[1::2] = [y * height for y in result[1::2]]
    return result


def _get_bbox_area(bbox):
    return (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])


@pytest.mark.usefixtures('new_clean_dir')
class TestObjectAnnotation:

    @staticmethod
    def _build_annotation(bbox):
        oa = ObjectAnnotation()
        oa.init({
            DatasetFieldLabels.CLASS_LABEL: "label1",
            DatasetFieldLabels.IS_CROWD: "false",
            DatasetFieldLabels.X_0_PERCENT: bbox[0],
            DatasetFieldLabels.Y_0_PERCENT: bbox[1],
            DatasetFieldLabels.X_1_PERCENT: bbox[2],
            DatasetFieldLabels.Y_1_PERCENT: bbox[3]
        })
        return oa

    @staticmethod
    def _test_annotation(bbox, expected_valid):
        height = 600
        width = 900
        annotation = TestObjectAnnotation._build_annotation(bbox)
        assert annotation.valid == expected_valid
        assert annotation.label == "label1"
        assert annotation.iscrowd == 0
        annotation_box = [annotation._x0_percentage, annotation._y0_percentage,
                          annotation._x1_percentage, annotation._y1_percentage]
        assert annotation_box == bbox
        assert annotation.missing_properties
        assert not annotation._normalized_mask_poly
        assert not annotation.has_valid_mask
        if expected_valid:
            annotation.fill_box_properties(height=height, width=width)
            assert not annotation.missing_properties
            assert not annotation.has_valid_mask
            pixel_bbox = _get_pixel_bbox(bbox, height, width)
            assert annotation.bounding_box == pixel_bbox
            assert annotation.area == _get_bbox_area(pixel_bbox)
            assert annotation.rle_masks is None

    def test_annotation_default(self):
        bbox = [0.0, 0.0, 0.5, 0.5]
        self._test_annotation(bbox, True)

    def test_annotation_missing_fields(self):
        bbox = [0.0, 0.0, 0.5, 0.5]
        # DatasetFieldLabels.CLASS_LABEL missing
        with pytest.raises(AutoMLVisionDataException):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.X_0_PERCENT: bbox[0],
                DatasetFieldLabels.Y_0_PERCENT: bbox[1],
                DatasetFieldLabels.X_1_PERCENT: bbox[2],
                DatasetFieldLabels.Y_1_PERCENT: bbox[3]
            })
            return oa

        # DatasetFieldLabels.X_0_PERCENT missing
        with pytest.raises(AutoMLVisionDataException):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.CLASS_LABEL: "label1",
                DatasetFieldLabels.Y_0_PERCENT: bbox[1],
                DatasetFieldLabels.X_1_PERCENT: bbox[2],
                DatasetFieldLabels.Y_1_PERCENT: bbox[3]
            })
            return oa

        # DatasetFieldLabels.Y_0_PERCENT missing
        with pytest.raises(AutoMLVisionDataException):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.CLASS_LABEL: "label1",
                DatasetFieldLabels.X_0_PERCENT: bbox[0],
                DatasetFieldLabels.X_1_PERCENT: bbox[2],
                DatasetFieldLabels.Y_1_PERCENT: bbox[3]
            })
            return oa

        # DatasetFieldLabels.X_1_PERCENT missing
        with pytest.raises(AutoMLVisionDataException):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.CLASS_LABEL: "label1",
                DatasetFieldLabels.X_0_PERCENT: bbox[0],
                DatasetFieldLabels.Y_0_PERCENT: bbox[1],
                DatasetFieldLabels.Y_1_PERCENT: bbox[3]
            })
            return oa

        # DatasetFieldLabels.Y_1_PERCENT missing
        with pytest.raises(AutoMLVisionDataException):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.CLASS_LABEL: "label1",
                DatasetFieldLabels.X_0_PERCENT: bbox[0],
                DatasetFieldLabels.Y_0_PERCENT: bbox[1],
                DatasetFieldLabels.X_1_PERCENT: bbox[2]
            })
            return oa

    def test_annotation_invalid_bbox(self):
        # Values < 0.0
        bbox = [-0.1, 0.0, 0.5, 0.5]
        self._test_annotation(bbox, False)
        # Values > 1.0
        bbox = [0.0, 0.0, 0.5, 1.1]
        self._test_annotation(bbox, False)
        # some values < 0.0 and some values > 1.0
        bbox = [0.0, -0.1, 1.1, 0.5]
        self._test_annotation(bbox, False)
        # x0 > x1
        bbox = [0.8, 0.0, 0.5, 0.5]
        self._test_annotation(bbox, False)
        # x0 = x1
        bbox = [0.5, 0.0, 0.5, 0.5]
        self._test_annotation(bbox, False)
        # y0 > y1
        bbox = [0.0, 0.8, 0.5, 0.5]
        self._test_annotation(bbox, False)
        # y0 = y1
        bbox = [0.0, 0.5, 0.5, 0.5]
        self._test_annotation(bbox, False)

    def test_annotation_none_class(self):
        with pytest.raises(
            AutoMLVisionDataException,
            match=re.escape(
                "Expected a string or an integer for the class field, e.g.\n"
                "\"label\": [{\"label\": \"cat\", \"topX\": 0.1, \"bottomX\": 0.2, \"topY\": 0.3, \"bottomY\": 0.4, "
                "\"isCrowd\": 0}]\nor\n"
                "\"label\": [{\"label\": 1, \"topX\": 0.1, \"bottomX\": 0.2, \"topY\": 0.3, \"bottomY\": 0.4, "
                "\"isCrowd\": 0}]\n. Found type <class 'NoneType'>."
            )
        ):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.CLASS_LABEL: None,
                DatasetFieldLabels.X_0_PERCENT: 0.1,
                DatasetFieldLabels.Y_0_PERCENT: 0.2,
                DatasetFieldLabels.X_1_PERCENT: 0.3,
                DatasetFieldLabels.Y_1_PERCENT: 0.4
            })

    def test_annotation_integer_class(self):
        oa = ObjectAnnotation()
        oa.init({
            DatasetFieldLabels.CLASS_LABEL: 42,
            DatasetFieldLabels.X_0_PERCENT: 0.1,
            DatasetFieldLabels.Y_0_PERCENT: 0.2,
            DatasetFieldLabels.X_1_PERCENT: 0.3,
            DatasetFieldLabels.Y_1_PERCENT: 0.4
        })

    def test_annotation_float_class(self):
        with pytest.raises(
            AutoMLVisionDataException,
            match=re.escape(
                "Expected a string or an integer for the class field, e.g.\n"
                "\"label\": [{\"label\": \"cat\", \"topX\": 0.1, \"bottomX\": 0.2, \"topY\": 0.3, \"bottomY\": 0.4, "
                "\"isCrowd\": 0}]\nor\n"
                "\"label\": [{\"label\": 1, \"topX\": 0.1, \"bottomX\": 0.2, \"topY\": 0.3, \"bottomY\": 0.4, "
                "\"isCrowd\": 0}]\n. Found type <class 'float'>."
            )
        ):
            oa = ObjectAnnotation()
            oa.init({
                DatasetFieldLabels.CLASS_LABEL: 2.3,
                DatasetFieldLabels.X_0_PERCENT: 0.1,
                DatasetFieldLabels.Y_0_PERCENT: 0.2,
                DatasetFieldLabels.X_1_PERCENT: 0.3,
                DatasetFieldLabels.Y_1_PERCENT: 0.4
            })


@pytest.mark.usefixtures('new_clean_dir')
class TestObjectAnnotationWithPolygon:

    @staticmethod
    def _build_annotation(polygon):
        oa = ObjectAnnotation()
        oa.init({
            DatasetFieldLabels.CLASS_LABEL: "label1",
            DatasetFieldLabels.POLYGON: polygon,
            DatasetFieldLabels.IS_CROWD: "false"
        })
        return oa

    @staticmethod
    def _calulate_bbox(polygon):
        x_min_percent, x_max_percent, y_min_percent, y_max_percent = 101., -1., 101., -1.
        if polygon and polygon[0]:
            for segment in polygon:
                xs = segment[::2]
                ys = segment[1::2]
                x_min_percent = min(x_min_percent, min(xs))
                x_max_percent = max(x_max_percent, max(xs))
                y_min_percent = min(y_min_percent, min(ys))
                y_max_percent = max(y_max_percent, max(ys))
        return [x_min_percent, y_min_percent, x_max_percent, y_max_percent]

    @staticmethod
    def _get_pixel_polygon(normalized_poly, height, width):
        result = copy.deepcopy(normalized_poly)
        for segment in result:
            segment[::2] = [x * width for x in segment[::2]]
            segment[1::2] = [y * height for y in segment[1::2]]
        return result

    @staticmethod
    def _test_annotation(polygon, expected_poygon, expected_valid):
        height = 600
        width = 900
        annotation = TestObjectAnnotationWithPolygon._build_annotation(polygon)
        assert annotation.valid == expected_valid
        assert annotation.label == "label1"
        assert annotation.iscrowd == 0
        assert annotation._normalized_mask_poly == expected_poygon
        annotation_box = [annotation._x0_percentage, annotation._y0_percentage,
                          annotation._x1_percentage, annotation._y1_percentage]
        expected_box = TestObjectAnnotationWithPolygon._calulate_bbox(expected_poygon)
        assert annotation_box == expected_box
        assert annotation.missing_properties
        assert annotation.rle_masks is None
        assert annotation.has_valid_mask == expected_valid
        if expected_valid:
            # Fill box properties
            annotation.fill_box_properties(height=height, width=width)
            assert not annotation.missing_properties
            assert annotation._mask_poly == \
                TestObjectAnnotationWithPolygon._get_pixel_polygon(expected_poygon, height, width)
            assert annotation.rle_masks is not None
            assert annotation.has_valid_mask
            expected_pixel_bbox = _get_pixel_bbox(expected_box, height, width)
            assert annotation.bounding_box == expected_pixel_bbox
            assert annotation.area == _get_bbox_area(expected_pixel_bbox)

    def test_annotation_default(self):
        polygon = [[0.0, 0.0, 0.0, 0.5, 0.5, 0.5]]
        self._test_annotation(polygon, polygon, True)

        polygon = [[0.0, 0.0, 0.0, 0.5, 0.5, 0.5], [0.5, 0.5, 0.5, 0.0, 0.0, 0.0]]
        self._test_annotation(polygon, polygon, True)

    def test_annotation_missing_fields(self):
        # DatasetFieldLabels.CLASS_LABEL missing
        with pytest.raises(AutoMLVisionDataException):
            ObjectAnnotation().init({DatasetFieldLabels.POLYGON: [[0.0, 0.0, 0.0, 0.5, 0.5, 0.5]]})
        # DatasetFieldLabels.POLYGON missing
        with pytest.raises(AutoMLVisionDataException):
            ObjectAnnotation().init({DatasetFieldLabels.CLASS_LABEL: "label1"})

    def test_annotation_empty_polygon(self):
        self._test_annotation(None, None, False)
        self._test_annotation([], [], False)
        self._test_annotation([[]], [[]], False)

    def test_annotation_polygon_odd_elements(self):
        with pytest.raises(AutoMLVisionDataException):
            self._build_annotation([[0.0, 0.0, 0.0, 0.5, 0.5]])

        with pytest.raises(AutoMLVisionDataException):
            self._build_annotation([[0.0, 0.0, 0.0, 0.5, 0.5],
                                    [0.0, 0.0, 0.0, 0.5, 0.5, 0.5]])

    def test_annotation_all_segments_invalid(self):
        # Single polygon segment with len < 5
        polygon = [[0.17, 0.29, 0.19, 0.29]]
        self._test_annotation(polygon, [], False)

        # Single polygon segment with values < 0.0
        polygon = [[-0.1, 0.2, 0.3, 0.5, 1.0, 1.0]]
        self._test_annotation(polygon, [], False)

        # Single polygon segment with values > 1.0
        polygon = [[0.1, 0.2, 0.3, 0.5, 1.0, 1.1]]
        self._test_annotation(polygon, [], False)

        # Multiple invalid segments
        polygon = [[0.17, 0.29, 0.19, 0.29],  # len < 5
                   [-0.1, 0.2, 0.3, 0.5, 1.0, 1.0],  # has values < 0.0
                   [0.1, 0.2, 0.3, 0.5, 1.0, 1.1],  # has values > 1.0
                   ]
        self._test_annotation(polygon, [], False)

    def test_annotation_some_segments_invalid(self):
        valid_segment = [0.0, 0.0, 0.0, 0.5, 0.5, 0.5]
        # Invalid polygon segment with len < 5
        polygon = [[0.17, 0.29, 0.19, 0.29], valid_segment]
        self._test_annotation(polygon, [valid_segment], True)

        # Invalid polygon segment with values < 0.0
        polygon = [valid_segment, [-0.1, 0.2, 0.3, 0.5, 1.0, 1.0]]
        self._test_annotation(polygon, [valid_segment], True)

        # Invalid polygon segment with values > 1.0
        polygon = [[0.1, 0.2, 0.3, 0.5, 1.0, 1.1], valid_segment]
        self._test_annotation(polygon, [valid_segment], True)

        # Multiple invalid segments and one valid segment
        polygon = [[0.17, 0.29, 0.19, 0.29],  # len < 5
                   [-0.1, 0.2, 0.3, 0.5, 1.0, 1.0],  # has values < 0.0
                   valid_segment,
                   [0.1, 0.2, 0.3, 0.5, 1.0, 1.1],  # has values > 1.0
                   ]
        self._test_annotation(polygon, [valid_segment], True)

    def test_annotation_segments_valid_bbox_invalid(self):
        polygon = [[0.5, 0.6, 0.5, 0.7, 0.5, 0.8]]
        self._test_annotation(polygon, polygon, False)

        polygon = [[0.5, 0.5, 0.6, 0.5, 0.7, 0.5]]
        self._test_annotation(polygon, polygon, False)

        polygon = [[0.5, 0.5, 0.5, 0.5, 0.5, 0.5]]
        self._test_annotation(polygon, polygon, False)
