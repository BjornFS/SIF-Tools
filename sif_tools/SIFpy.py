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
        Specify the window for slicing the data. The window slices around the center wavelength:
        - 'reduced': slices 10% of entries from each end
        - 'narrow' : slices 25% of entries from each end
        - 'pinched'    : slices 33% of entries from each end

    Returns:
    -------
    numpy.ndarray
        A NumPy array containing the combined spectral data from the SIF file(s).
        Each row corresponds to a pair of wavelength and count.

    Examples:
    ---------
    To use the full data without slicing:
        convert_sif_to_array(target='path/to/sif', reduce_noise=True, window=None)

    To slice the first 100 data points:
        convert_sif_to_array(target='path/to/sif', reduce_noise=True, window='0:100')

    To slice from the 50th to the 200th data point:
        convert_sif_to_array(target='path/to/sif', reduce_noise=True, window='50:200')
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
