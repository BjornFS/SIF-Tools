"""
conversion.py

Module for converting Spectral Image Format (SIF) files into NumPy arrays.
Supports both individual files and directories of files.
"""

import os
from typing import List
import numpy as np

from .source import source


def SIFconvert(target: str) -> np.ndarray:
    """
    Convert SIF (Spectral Image Format) files to a NumPy array.

    Parameters
    ----------
    target : str
        Path to a SIF file or a directory containing SIF files.

    Returns
    -------
    np.ndarray
        A NumPy array containing stacked wavelength and count data
        from the processed SIF files.

    Raises
    ------
    RuntimeError
        If any error occurs during the file processing.
    """
    try:
        paths: List[str] = _get_paths(target)
        data_list: List[np.ndarray] = []

        for path in paths:
            data, _ = source.parse(path)
            wavelengths, counts = data[:, 0], data[:, 1]
            # Combine wavelengths and counts into a 2D array
            data_list.append(np.column_stack((wavelengths, counts)))

        # Return single array if only one file, else stack vertically
        return data_list[0] if len(data_list) == 1 else np.vstack(data_list)

    except Exception as e:
        raise RuntimeError(f"An error occurred while converting SIF to array: {str(e)}")


def _get_paths(target: str) -> List[str]:
    """
    Retrieve file paths from the given target.

    Parameters
    ----------
    target : str
        Path to a file or directory.

    Returns
    -------
    List[str]
        List of file paths.

    Raises
    ------
    ValueError
        If target is neither a file nor a directory.
    """
    if os.path.isfile(target):
        return [target]
    elif os.path.isdir(target):
        return source.extract_files_from_folder(target)
    else:
        raise ValueError("Target must be a file or directory.")