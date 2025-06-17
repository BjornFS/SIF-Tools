"""
source.py

Utility class for handling SIF file operations: parsing, calibration extraction,
folder extraction, and optional info printing.
"""

import os
import typing
from collections import OrderedDict

import numpy as np

try:
    from .parser import parser
    from .calibration import extract_calibration
except ImportError as e:
    raise e


class source:
    """Utility class for handling SIF file operations."""

    @staticmethod
    def parse(file: str) -> typing.Tuple[np.ndarray, OrderedDict]:
        """
        Parse a .sif file.

        Parameters
        ----------
        file : str
            Path to a .sif file.

        Returns
        -------
        Tuple[np.ndarray, OrderedDict]
            A tuple containing:
                - A 2D NumPy array (shape: 2 * channels) where first column contains wavelengths 
                  and second contains counts.
                - An OrderedDict with measurement metadata.
        """
        data, info = parser(file)
        wavelengths = extract_calibration(info)

        flat_data = data.flatten()
        df = np.column_stack((wavelengths, flat_data))
        return df, info

    @staticmethod
    def extract_files_from_folder(path: str, file_extension: str = '.sif') -> typing.List[str]:
        """
        Extract files with a specific extension from a folder.

        Parameters
        ----------
        path : str
            Path to the folder.
        file_extension : str, optional
            File extension to filter by (default is '.sif').

        Returns
        -------
        List[str]
            Sorted list of filenames with the specified extension.
        """
        files = os.listdir(path)
        SIFfiles = [f for f in files if f.endswith(file_extension)]
        SIFfiles.sort()
        return SIFfiles

    @staticmethod
    def extract_info(info: OrderedDict, show_info: str) -> None:
        """
        Optionally print the info based on the flag show_info.

        Parameters
        ----------
        info : OrderedDict
            Contains file information.
        show_info : str
            String flag to indicate whether to print the info ('true' to print).
        """
        if show_info.lower() == 'true':
            for key, value in info.items():
                print(f"{key}: {value}")