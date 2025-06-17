"""
calibration.py

Functions for extracting calibration data from SIF file metadata.
"""

import typing
from collections import OrderedDict

import numpy as np


def extract_calibration(info: OrderedDict) -> typing.Optional[np.ndarray]:
    """
    Extract calibration data from file metadata.

    Parameters
    ----------
    info : OrderedDict
        Metadata dictionary produced by read_file().

    Returns
    -------
    Optional[np.ndarray]
        - 1D NumPy array of size [width] if a single calibration is found.
        - 2D NumPy array of size [NumberOfFrames x width] if multiple calibrations are found.
        - None if no calibration data exists.
    """
    width: int = info['DetectorDimensions'][0]

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