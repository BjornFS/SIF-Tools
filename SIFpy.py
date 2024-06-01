import os
import numpy as np

from utils import MATH, FILE

class sif2array:
    def __init__(self, target, reduce_noise=False, window=None):
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
            self.data = data_list[0]
        else:
            self.data = np.vstack(data_list)

    def get_data(self):
        return self.data