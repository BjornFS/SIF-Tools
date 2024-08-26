# A utility for generating heatmaps from hyperspectral data.
#
# This class provides methods to process a directory of spectral files along with a background file.
# It handles noise reduction, data slicing, and heatmap creation.
#
# Functions:
#   hyperspectrum:
#       Generates a heatmap from hyperspectral data by processing the files in the specified directory.
#
#   _validate_inputs:
#       Validates the input directory and background file.
#
#   _get_files:
#       Retrieves and filters the list of spectrum files in the directory, excluding the background file.
#
#   _process_background:
#       Processes the background file data.
#
#   _process_files:
#       Processes each spectrum file and computes adjusted counts after background subtraction.
#
#   _create_heatmap:
#       Creates a 2D heatmap grid based on the processed pixel values.
#
# @Bjørn Funch Schrøder Nielsen

import os
import numpy as np
from scipy.interpolate import interp1d

from .utils import MATH, FILE

    
@staticmethod
def hyperspectrum(directory     : str, 
                  background    : str, 
                  size          : tuple[int, int], 
                  method        : str  = 'integration', # could also be 'max'
                  window        : str  = 'narrow', # or 'reduced' or 'pinched'
                  reduce_noise  : bool = True,
                  normalize     : bool = False):
    """ Generates a NxM heatmap from hyperspectral data.

    Parameters:

        `directory`
            Directory containing spectrum files.
        `background`
            Filename of the background spectrum file.
        `size`
            Image stitching scheme, e.g. 25 datapoints: tuple(5,5)
        `method`
            notImplemented
        `window` (optional)
            The window of data to be sliced for plotting. Defaults to `narrow`.
        `reduce_noise` (optional)
            Reduce extreme noise peaks, using a `N sigma-gradient` approach.
        `normalize` (optional)
            Normalize the hyperspectrum plot data.

    Returns:

        2D array representing the heatmap data.
    """
    try:
        _validate_inputs(directory, background)

        files = _get_files(directory, background)
        background_data = _process_background(directory, background, window, reduce_noise)

        pixels = _process_files(directory, files, background_data, window, reduce_noise)
        
        if normalize:
            pixels = MATH.normalize_array(np.array(pixels))

        heatmap_data = _create_heatmap(size, pixels)

        return heatmap_data

    except Exception as e:
        raise RuntimeError(f"An error occurred while generating the heatmap: {str(e)}")

@staticmethod
def _validate_inputs(directory, background):
    """ Validates the input directory and background file.

    Parameters:

        `directory`
            Directory containing spectrum files.
        `background`
            Filename of the background spectrum file.

    Raises:

        `ValueError`: directory is not valid.
        `FileNotFoundError`: background file not in the directory.
    """
    if not os.path.isdir(directory):
        raise ValueError("'directory' parameter has to be a directory, not a file.")

    if not os.path.isfile(os.path.join(directory, background)):
        raise FileNotFoundError(f"Background file '{background}' not found in the directory.")

@staticmethod
def _get_files(directory, background):
    """ Retrieves and filters the list of spectrum files in the directory, excluding the background file.

    Parameters:

        `directory`
            Directory containing spectrum files.
        `background `
            Filename of the background spectrum file.

    Returns:

        List of spectrum files excluding the background file.
    """
    files = FILE.extract_files_from_folder(directory)
    files.remove(os.path.basename(background))  # Remove background file from list of files
    return files

@staticmethod
def _process_background(directory, background, window, reduce_noise):
    """ Processes the background file data.

    Parameters:

        `directory`
            Directory containing spectrum files.
        `background`
            Filename of the background spectrum file.
        `window`
            The window of data to be sliced for plotting.
        `reduce_noise`
            Whether to reduce noise in the data.

    Returns:

        Processed background wavelengths and counts as tuple.
    """
    background_data, _ = FILE.parse(os.path.join(directory, background))
    background_data = MATH.slice_window(background_data, window=window)
    bg_wavelengths, bg_counts = background_data[:, 0], background_data[:, 1]

    if reduce_noise:
        bg_wavelengths, bg_counts = MATH.gradient_n_sigma(bg_wavelengths, bg_counts)

    return bg_wavelengths, bg_counts

@staticmethod
def _process_files(directory, files, background_data, window, reduce_noise):
    """ Processes each spectrum file and computes adjusted counts after background subtraction.

    Parameters:

        `directory`
            Directory containing spectrum files.
        `files`
            List of spectrum files to be processed.
        `background_data`
            Processed background wavelengths and counts.
        `window`
            The window of data to be sliced for plotting.
        `reduce_noise`
            Whether to reduce noise in the data.

    Returns:

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
def _create_heatmap(size, normalized_pixels):
    """ Creates a 2D heatmap grid based on the processed pixel values.

    Parameters:

        `size`
            Image stitching scheme, e.g. 25 datapoints: tuple(5,5)
        `normalized_pixels`
            Normalized pixel values representing adjusted counts for each file.

    Returns:

        A 2D array representing the heatmap data.
    """
    max_x, max_y = size  # Unpack the size tuple into dimensions
    heatmap_data = np.zeros((max_y, max_x))  # Create an empty grid for the heatmap
    
    # Ensure the number of normalized pixels matches the total number of grid cells
    if len(normalized_pixels) != max_x * max_y:
        raise ValueError(f"Number of normalized_pixels ({len(normalized_pixels)}) does not match size {max_x * max_y}.")

    # Fill the heatmap with the normalized pixel values
    for index, value in enumerate(normalized_pixels):
        row = index // max_x  # Determine the row index
        col = index % max_x   # Determine the column index
        heatmap_data[row, col] = value  # Assign the pixel value to the heatmap

    return heatmap_data
