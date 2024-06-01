import typing
import numpy as np
import os
from collections import OrderedDict
from SIFopen import read_file


def extract_calibration(info: OrderedDict) -> typing.Optional[np.ndarray]:
    """
    Extract calibration data from info.

    Parameters
    ----------
    info: OrderedDict
        OrderedDict from read_file()

    Returns
    -------
    calibration: np.ndarray or None
        1D array of size [width] if only one calibration is found.
        2D array of size [NumberOfFrames x width] if multiple calibrations are found.
        None if no calibration is found.
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


def return_info(info: OrderedDict, show_info: str) -> None:
    """
    Optionally print the info based on the flag show_info.

    Parameters
    ----------
    info: OrderedDict
        OrderedDict containing the file information.
    
    show_info: str
        String flag to indicate whether to print the info. Should be 'true' to print.
    """
    if show_info.lower() == 'true':
        for key, value in info.items():
            print(f"{key}: {value}")


def parse(file: str) -> typing.Tuple[np.ndarray, OrderedDict]:
    """
    Parse a .sif file.

    Parameters
    ----------
    file: str
        Path to a .sif file.
    
    Returns
    -------
    tuple: (np.ndarray, OrderedDict)
        A tuple containing:
        - A 2D numpy array (channels x 2) with the first element of each row being the wavelength bin and the second being the counts.
        - An OrderedDict with information about the measurement.
    """
    data, info = read_file(file)
    wavelengths = extract_calibration(info)

    flat_data = data.flatten()

    if wavelengths.size != flat_data.size:
        flat_data = data[0].flatten()

    df = np.column_stack((wavelengths, flat_data))
    return df, info


def extract_files_from_folder(path: str, file_extension: str = '.sif') -> typing.List[str]:
    """
    Extract files with a specific extension from a folder.

    Parameters
    ----------
    path: str
        Path to the folder.
    
    file_extension: str, optional
        File extension to filter by (default is '.sif').
    
    Returns
    -------
    list: List[str]
        A list of filenames with the specified extension.
    """
    return [f for f in os.listdir(path) if f.endswith(file_extension)]


def gradient_n_sigma(wavelengths: np.ndarray, counts: np.ndarray, sigma: int = 3) -> typing.Tuple[np.ndarray, np.ndarray]:
    """
    Remove spikes from data using a gradient method with n-sigma threshold.

    Parameters
    ----------
    wavelengths: np.ndarray
        Array of wavelength data.
    
    counts: np.ndarray
        Array of count data.
    
    sigma: int, optional
        Number of standard deviations to use for filtering (default is 3).
    
    Returns
    -------
    tuple: (np.ndarray, np.ndarray)
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
    """
    Parse the data and handle the specified window case.

    Parameters
    ----------
    data: np.ndarray
        Data array to be sliced.
    
    window: str
        Type of windowing to apply. Options are 'narrow', 'reduced', 'SHG'.
    
    Returns
    -------
    np.ndarray
        The sliced data array.
    """
    if window == 'narrow':
        remove_count = len(data) // 4
        data = data[remove_count:-remove_count]

    elif window == 'reduced':
        remove_count = len(data) // 10
        data = data[remove_count:-remove_count]

    elif window == 'SHG':
        remove_count = len(data) // 3
        data = data[remove_count:-remove_count]

    return data
