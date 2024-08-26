import typing
import os
from collections import OrderedDict

import numpy as np

try:
    from .SIFopen import read_file
except:
    try:
        from SIFopen import read_file
    except:
        raise


class FILE:
    """ A utility class for handling SIF file operations, including extracting calibration data, 
    parsing SIF files, and extracting files from folders.

    Methods:
    
        extract_calibration(info)
            Extract calibration data from info.

        parse(file)
            Parse a .sif file.

        extract_files_from_folder(path, file_extension)
            Extract files with a specific extension from a folder.

        extract_info(info, show_info)
            Optionally print the info based on the flag show_info.
    """

    def extract_calibration(info: OrderedDict) -> typing.Optional[np.ndarray]:
        """ Extract calibration data from info.

        Parameters:

            `info`
                OrderedDict from read_file()

        Returns:

            `calibration`
                * 1D array of size [width] if only one calibration is found.
                * 2D array of size [NumberOfFrames x width] if multiple calibrations.
                * None if no calibration is found.
        """
        width = info['DetectorDimensions'][0]
        
        if 'Calibration_data_for_frame_1' in info:
            calibration = np.ndarray((info['NumberOfFrames'], width))
            for f in range(info['NumberOfFrames']):
                key = f'Calibration_data_for_frame_{f + 1}'
                flip_coef = np.flipud(info[key])
                calibration[f] = np.poly1d(flip_coef)(np.arange(1, width + 1))
            return calibration

        elif 'Calibration_data' in info:
            flip_coef = np.flipud(info['Calibration_data'])
            return np.poly1d(flip_coef)(np.arange(1, width + 1))
        
        return None

    def parse(file: str) -> typing.Tuple[np.ndarray, OrderedDict]:
        """ Parse a .sif file.
        
        Parameters:

            `file`
                Path to a .sif file.
        
        Returns:

            A tuple containing:
                * A 2D numpy array (2*channels) with 1st element of row i == wavelengths and 2nd == counts.
                * An OrderedDict with information about the measurement.
        """
        data, info = read_file(file)
        wavelengths = FILE.extract_calibration(info)

        flat_data = data.flatten()

        df = np.column_stack((wavelengths, flat_data))
        return df, info


    def extract_files_from_folder(path: str, file_extension: str = '.sif') -> typing.List[str]:
        """ Extract files with a specific extension from a folder.

        Parameters:

            `path`
                Path to the folder.
            `file_extension`
                File extension to filter by (default is '.sif').
        
        Returns:

            A list of filenames with the specified extension.
        """
        return [f for f in os.listdir(path) if f.endswith(file_extension)].sort()

    def extract_info(info: OrderedDict, show_info: str) -> None:
        """ Optionally print the info based on the flag show_info.

        Parameters:

            `info`
                OrderedDict containing the file information.
            
            `show_info`
                String flag to indicate whether to print the info.
        """
        if show_info.lower() == 'true':
            for key, value in info.items():
                print(f"{key}: {value}")


class MATH:
    """ A utility class for handling mathematical operations on spectral data, including noise reduction,
    data slicing, and normalization.

    Methods:

        gradient_n_sigma(wavelengths: np.ndarray, counts: np.ndarray, sigma)
            Remove spikes from data using a gradient method with n-sigma threshold.

        slice_window(data: np.ndarray, window: str)
            Parse the data and handle the specified window case.

        normalize_array(array: np.ndarray)
            Normalize an array to the range [0, 1].
    """
    def gradient_n_sigma(wavelengths: np.ndarray, counts: np.ndarray, sigma: int = 3) -> typing.Tuple[np.ndarray, np.ndarray]:
        """ Remove spikes from data using a gradient method with n-sigma threshold. 
                    
        Parameters:

            `wavelengths`
                Array of wavelength data.
            `counts`
                Array of count data.
            `sigma` (optional)
                Number of standard deviations to use for filtering (default is 3).
        
        Returns:

            A tuple containing filtered wavelength and count data.
        """
        gradients = np.diff(counts)
        mean_gradient = np.mean(gradients)
        std_gradient = np.std(gradients)
        threshold = sigma * std_gradient
        spike_indices = np.where(np.abs(gradients - mean_gradient) > threshold)[0]

        filtered_wavelengths = np.delete(wavelengths, spike_indices + 1)  # +1 to correct the shift caused by np.diff
        filtered_counts = np.delete(counts, spike_indices + 1)

        return filtered_wavelengths, filtered_counts


    def slice_window(data: np.ndarray, window: str) -> np.ndarray:
        """ Parse the data and handle the specified window case.

        Parameters:

            `data`
                Array to be sliced.
            `window`
                `reduced` : removes 10% of entries from head and tail.
                `narrow`  : 25%
                `pinched` : 33%
        
        Returns

            The sliced np.ndarray.
        """

        if window == 'reduced':
            remove_count = len(data) // 10
            data = data[remove_count:-remove_count]
        
        elif window == 'narrow':
            remove_count = len(data) // 4
            data = data[remove_count:-remove_count]

        elif window == 'pinched':
            remove_count = len(data) // 3
            data = data[remove_count:-remove_count]

        return data

    def normalize_array(array):
        array_min = np.min(array)
        array_max = np.max(array)
        
        # Avoid division by zero in case the array is constant
        if array_max - array_min == 0:
            return np.zeros_like(array)
        
        normalized_array = (array - array_min) / (array_max - array_min)
        return normalized_array