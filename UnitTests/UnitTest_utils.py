import unittest
from collections import OrderedDict
import numpy as np
from sif_tools.utils import FILE, MATH
from sif_tools.SIFopen import read_file

#python -m unittest discover -s tests

class TestFILE(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'UnitTests/UnitTest files'
        cls.background_file = 'test_background.sif'
        cls.test_files = [f'test_{i}.sif' for i in range(1, 16+1)]
        cls.test_files.append(cls.background_file)
    
    def test_extract_calibration_single(self):
        info_single = OrderedDict({
            'DetectorDimensions': [100],
            'Calibration_data': [1, 0]
        })
        expected_output = np.arange(1, 101)
        calibration = FILE.extract_calibration(info_single)
        np.testing.assert_array_equal(calibration, expected_output)

    def test_extract_calibration_multi(self):
        info_multi = OrderedDict({
            'DetectorDimensions': [100],
            'NumberOfFrames': 2,
            'Calibration_data_for_frame_1': [1, 0],
            'Calibration_data_for_frame_2': [1, 0]
        })
        expected_output = np.array([np.arange(1, 101), np.arange(1, 101)])
        calibration = FILE.extract_calibration(info_multi)
        np.testing.assert_array_equal(calibration, expected_output)

    def test_extract_files_from_folder(self):
        extracted_files = FILE.extract_files_from_folder(self.test_dir)
        self.assertCountEqual(extracted_files, self.test_files)

    def test_extract_positions(self):
        files = ['file_1_0_0.sif', 'file_2_1_1.sif', 'file_3_2_2.sif']
        expected_positions = [0, 1, 2]
        positions = FILE.extract_positions(files)
        self.assertEqual(positions, expected_positions)

    def test_extract_info(self):
        info = OrderedDict({'key1': 'value1', 'key2': 'value2'})
        with self.assertLogs(level='INFO') as log:
            FILE.extract_info(info, 'true')
            self.assertIn('INFO:root:key1: value1', log.output)
            self.assertIn('INFO:root:key2: value2', log.output)

class TestMATH(unittest.TestCase):

    def test_gradient_n_sigma(self):
        wavelengths = np.array([1, 2, 3, 4, 5, 6])
        counts = np.array([1, 100, 3, 4, 100, 6])
        expected_wavelengths = np.array([1, 3, 4, 6])
        expected_counts = np.array([1, 3, 4, 6])
        filtered_wavelengths, filtered_counts = MATH.gradient_n_sigma(wavelengths, counts)
        np.testing.assert_array_equal(filtered_wavelengths, expected_wavelengths)
        np.testing.assert_array_equal(filtered_counts, expected_counts)

    def test_slice_window(self):
        data = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        expected_reduced = np.array([2, 3, 4, 5, 6, 7, 8, 9])
        expected_narrow = np.array([3, 4, 5, 6, 7, 8])
        expected_pinched = np.array([4, 5, 6, 7])
        np.testing.assert_array_equal(MATH.slice_window(data, 'reduced'), expected_reduced)
        np.testing.assert_array_equal(MATH.slice_window(data, 'narrow'), expected_narrow)
        np.testing.assert_array_equal(MATH.slice_window(data, 'pinched'), expected_pinched)

    def test_normalize_array(self):
        array = np.array([1, 2, 3, 4, 5])
        expected_output = np.array([0, 0.25, 0.5, 0.75, 1])
        normalized_array = MATH.normalize_array(array)
        np.testing.assert_array_equal(normalized_array, expected_output)

if __name__ == '__main__':
    unittest.main()
