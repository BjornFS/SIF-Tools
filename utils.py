import typing
import numpy as np
import os

from SIFopen import read_file


def extract_calibration(info):
    """
    Extract calibration data from info.

    Parameters
    ----------
    info: OrderedDict
        OrderedDict from read_file()

    Returns
    -------
    calibration:
        np.ndarray.
        1d array sized [width] if only 1 calibration is found.
        2d array sized [NumberOfFrames x width] if multiple calibration is
            found.
        None if no calibration is found
    """
    width = info['DetectorDimensions'][0]
    # multiple calibration data is stored
    if 'Calibration_data_for_frame_1' in info:
        calibration = np.ndarray((info['NumberOfFrames'], width))
        for f in range(len(calibration)):
            key = 'Calibration_data_for_frame_{:d}'.format(f + 1)
            flip_coef = np.flipud(info[key])
            calibration[f] = np.poly1d(flip_coef)(np.arange(1, width + 1))
        return calibration

    elif 'Calibration_data' in info:
        flip_coef = np.flipud(info['Calibration_data'])
        return np.poly1d(flip_coef)(np.arange(1, width + 1))
    else:
        return None
    
@staticmethod
def return_info(info, show_info):
    if show_info.lower() == 'true':
        for key, value in info.items():
            #print(f"{key}: {value}")
            None


def parse(file: str) -> typing.Tuple[np.ndarray, typing.Dict]:
    """
    Parse a .sif file.

    :param file: Path to a `.sif` file.
    :returns tuple[numpy.ndarray, OrderedDict]: Tuple of (data, info) where
        `data` is an (channels x 2) array with the first element of each row
        being the wavelength bin and the second being the counts.
        `info` is an OrderedDict of information about the measurement.
    """


    """
    data, info = read_file(file)
    wavelengths = extract_calibration(info)

    # @todo: `data.flatten()` may not be compatible with
    #   multiple images or 2D images.
    df = np.column_stack((wavelengths, data.flatten()))
    return (df, info)
    """


    data, info = read_file(file)
    wavelengths = extract_calibration(info)

    flat_data = data.flatten()

    # Since its multi-channel, multiple sizes of (1x1) or (1x2) may be outputted
    # if this happens, select the correct input, such that:
    # (1x2x2048) -> (1x4096) becomes (1x1x2048) -> (1x2048)
    if wavelengths.size != flat_data.size:
        flat_data = data[0][-1].flatten()

    df = np.column_stack((wavelengths, flat_data))
    return (df, info)

@staticmethod
def extract_files_from_folder(path, file_extension = '.sif'):
        return [f for f in os.listdir(path[0]) if f.endswith(file_extension)]


def gradient_n_sigma(wavelengths, counts, sigma=3):
    """
    Remove spikes from data using a 3-sigma gradient method.

    Parameters:
    - wavelengths: array-like, wavelength data
    - counts: array-like, count data
    - sigma: number of standard deviations to use for filtering (default: 3)

    Returns:
    - filtered_wavelengths: array-like, filtered wavelength data
    - filtered_counts: array-like, filtered count data
    """
    # Calculate the gradients
    gradients = np.diff(counts)

    # Calculate the mean and standard deviation of the gradients
    mean_gradient = np.mean(gradients)
    std_gradient = np.std(gradients)

    # Identify points where the gradient is more than `sigma` standard deviations from the mean
    threshold = sigma * std_gradient
    spike_indices = np.where(np.abs(gradients - mean_gradient) > threshold)[0]

    # Filter out the spikes
    filtered_wavelengths = np.delete(wavelengths, spike_indices + 1)  # +1 to correct the shift caused by np.diff
    filtered_counts = np.delete(counts, spike_indices + 1)

    return filtered_wavelengths, filtered_counts

# Function to parse the data and handle the narrow window case
def slice_window(data, window:str):

    if window == 'narrow':
        # Calculate the number of entries to remove (25% from both ends)
        remove_count = len(data) // 4
        data = data[remove_count:-remove_count]

    elif window == 'reduced':
        # Calculate the number of entries to remove (10% from both ends)
        remove_count = len(data) // 10
        data = data[remove_count:-remove_count]

    elif window == 'SHG':
        # Calculate the number of entries to remove (30% from both ends)
        remove_count = len(data) // 3
        data = data[remove_count:-remove_count]

    return data