"""
A utility for processing SIF (Spectral Image Format) files and converting them into NumPy arrays.

This class provides methods to handle both individual SIF files and directories containing multiple SIF files.
It offers functionality to optionally reduce noise in the data and to slice the data according to a specified window.

Functions:
--------
- `sif2array`:
    Convert SIF files to a NumPy array. This method processes the SIF files from the specified target (file or directory),
    optionally reduces noise, and slices the data to a specified window.

- `_get_paths`:
    Helper method to determine if the target is a file or a directory and extract file paths accordingly.

"""

import os
import numpy as np

from .utils import MATH, FILE


@staticmethod
def sif2array(target: str, reduce_noise: bool = False, window: str = None):
    """
    Convert SIF (Spectral Image Format) files to a NumPy array.

    This function processes SIF files from a given target (file or directory),
    optionally reduces noise, and slices the data to a specified window.

    Parameters:

    - `target : str`
        Path to a SIF file or a directory containing SIF files.
    - `reduce_noise : bool, optional`
        If True, applies noise reduction to the data (default is False).
    - `window : str, optional`
        Specify the window for slicing the data. The window slices around the center wavelength:
        - 'reduced': slices 10% of entries from each end
        - 'narrow' : slices 25% of entries from each end
        - 'pinched': slices 33% of entries from each end

    Returns:

    - `numpy.ndarray`
        A NumPy array containing the combined spectral data from the SIF file(s).
        Each row corresponds to a pair of wavelength and count.
    """
    try:
        paths = _get_paths(target)

        data_list = []
        for path in paths:
            data, _ = FILE.parse(path)
            if window:
                data = MATH.slice_window(data, window=window)
            wavelengths, counts = data[:, 0], data[:, 1]
            if reduce_noise:
                wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)
            data_list.append(np.column_stack((wavelengths, counts)))

        return data_list[0] if len(data_list) == 1 else np.vstack(data_list)

    except Exception as e:
        raise RuntimeError(f"An error occurred while converting SIF to array: {str(e)}")

@staticmethod
def _get_paths(target):
    if os.path.isfile(target):
        return [target]
    elif os.path.isdir(target):
        return FILE.extract_files_from_folder(target)
    else:
        raise ValueError("Target must be a file or directory.")
