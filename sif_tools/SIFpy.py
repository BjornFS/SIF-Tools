import os
import numpy as np

from .utils import MATH, FILE

def sif2array(target, reduce_noise=False, window=None):
    """
    Convert SIF (Spectral Image Format) files to a NumPy array.

    This function processes SIF files from a given target (file or directory),
    optionally reduces noise, and slices the data to a specified window.

    Parameters:
    ----------
    target : str
        Path to a SIF file or a directory containing SIF files.
    reduce_noise : bool, optional
        If True, applies noise reduction to the data (default is False).
    window : str, optional
        Specify the window for slicing the data. If None, the full data is used (default is None).

    Returns:
    -------
    numpy.ndarray
        A NumPy array containing the combined spectral data from the SIF file(s).
        Each row corresponds to a pair of wavelength and count.
    """
    # Check if the target is a file or a directory
    if os.path.isfile(target):
        paths = [target]
    else:
        paths = FILE.extract_files_from_folder(target)

    data_list = []

    for path in paths:
        data, _ = FILE.parse(path)

        if window:
            data = MATH.slice_window(data, window=window)

        wavelengths, counts = data[:, 0], data[:, 1]

        if reduce_noise:
            wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)

        data_list.append(np.column_stack((wavelengths, counts)))

    # Combine all data arrays into one ndarray
    if len(data_list) == 1:
        return data_list[0]
    else:
        return np.vstack(data_list)
