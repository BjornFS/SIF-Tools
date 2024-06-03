"""
A utility for generating heatmaps from hyperspectral data.

This class provides methods to process a directory of spectral files along with a background file.
It handles noise reduction, data slicing, and heatmap creation.

Functions:
--------
`hyperspectrum`:
    Generates a heatmap from hyperspectral data by processing the files in the specified directory.

`_validate_inputs`:
    Validates the input directory and background file.

`_get_files`:
    Retrieves and filters the list of spectrum files in the directory, excluding the background file.

`_process_background`:
    Processes the background file data.

`_process_files`:
    Processes each spectrum file and computes adjusted counts after background subtraction.

`_create_heatmap`:
    Creates a 2D heatmap grid based on the processed pixel values.
"""

import os
import numpy as np
from scipy.interpolate import interp1d

from .utils import MATH, FILE

    
@staticmethod
def hyperspectrum(directory: str, background: str, size=tuple[int, int], reduce_noise=True, window='pinched'):
    """
    Generates a heatmap from hyperspectral data.

    Parameters:

    - `directory : str`
        Directory containing spectrum files.
    - `background : str`
        Filename of the background spectrum file.
    - `size : tuple`
        Distribution of images. If 25 images taken in 5x5, tuple should be (5,5).
    - `reduce_noise : bool, optional`
        Whether to reduce noise in the data. Defaults to True.
    - `window : str, optional`
        The window of data to be sliced for plotting. Defaults to 'pinched'.

    Returns:

    - `np.ndarray`
        A 2D array representing the heatmap data.
    """
    try:
        _validate_inputs(directory, background)

        files = _get_files(directory, background)
        background_data = _process_background(directory, background, window, reduce_noise)

        positions = FILE.extract_positions(files)
        pixels = _process_files(directory, files, background_data, window, reduce_noise)
        normalized_pixels = MATH.normalize_array(np.array(pixels))

        heatmap_data = _create_heatmap(size, positions, normalized_pixels)

        return heatmap_data

    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the heatmap: {str(e)}")

@staticmethod
def _validate_inputs(directory, background):
    """
    Validates the input directory and background file.

    Parameters:

    - `directory : str`
        Directory containing spectrum files.
    - `background : str`
        Filename of the background spectrum file.

    Raises:

    - `ValueError`
        If the directory is not valid.
    - `FileNotFoundError`
        If the background file is not found in the directory.
    """
    if not os.path.isdir(directory):
        raise ValueError("'directory' parameter has to be a directory, not a file.")

    if not os.path.isfile(os.path.join(directory, background)):
        raise FileNotFoundError(f"Background file '{background}' not found in the directory.")

@staticmethod
def _get_files(directory, background):
    """
    Retrieves and filters the list of spectrum files in the directory, excluding the background file.

    Parameters:

    - `directory : str`
        Directory containing spectrum files.
    - `background : str`
        Filename of the background spectrum file.

    Returns:

    - `list`
        List of spectrum files excluding the background file.
    """
    files = FILE.extract_files_from_folder(directory)
    files.remove(os.path.basename(background))  # Remove background file from list of files
    return files

@staticmethod
def _process_background(directory, background, window, reduce_noise):
    """
    Processes the background file data.

    Parameters:

    - `directory : str`
        Directory containing spectrum files.
    - `background : str`
        Filename of the background spectrum file.
    - `window : str`
        The window of data to be sliced for plotting.
    - `reduce_noise : bool`
        Whether to reduce noise in the data.

    Returns:

    - `tuple`
        Processed background wavelengths and counts.
    """
    background_data, _ = FILE.parse(os.path.join(directory, background))
    background_data = MATH.slice_window(background_data, window=window)
    bg_wavelengths, bg_counts = background_data[:, 0], background_data[:, 1]

    if reduce_noise:
        bg_wavelengths, bg_counts = MATH.gradient_n_sigma(bg_wavelengths, bg_counts)

    return bg_wavelengths, bg_counts

@staticmethod
def _process_files(directory, files, background_data, window, reduce_noise):
    """
    Processes each spectrum file and computes adjusted counts after background subtraction.

    Parameters:

    - `directory : str`
        Directory containing spectrum files.
    - `files : list`
        List of spectrum files to be processed.
    - `background_data : tuple`
        Processed background wavelengths and counts.
    - `window : str`
        The window of data to be sliced for plotting.
    - `reduce_noise : bool`
        Whether to reduce noise in the data.

    Returns:

    - `list`
        List of pixel values representing adjusted counts for each file.
    """
    bg_wavelengths, bg_counts = background_data
    pixels = []

    for file in files:
        data, _ = FILE.parse(os.path.join(directory, file))
        data = MATH.slice_window(data, window=window)
        wavelengths, counts = data[:, 0], data[:, 1]

        if reduce_noise:
            wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)

        bg_interp = interp1d(bg_wavelengths, bg_counts, kind='linear', bounds_error=False, fill_value=0)
        bg_counts_interpolated = bg_interp(wavelengths)
        adjusted_counts = np.maximum(counts - bg_counts_interpolated, 0)
        pixels.append(int(np.sum(adjusted_counts)))

    return pixels

@staticmethod
def _create_heatmap(size, positions, normalized_pixels):
    """
    Creates a 2D heatmap grid based on the processed pixel values.

    Parameters:

    - `size : tuple`
        Distribution of images. If 25 images taken in 5x5, tuple should be (5,5).
    - `positions : list`
        List of positions for each file.
    - `normalized_pixels : np.ndarray`
        Normalized pixel values representing adjusted counts for each file.

    Returns:

    - `np.ndarray`
        A 2D array representing the heatmap data.
    """
    max_x, max_y = size
    heatmap_data = np.zeros((max_y, max_x))

    for idx, count in zip(positions, normalized_pixels):
        x = (idx - 1) % max_x
        y = (idx - 1) // max_x
        heatmap_data[y, x] = count

    return heatmap_data
