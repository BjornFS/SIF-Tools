import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import os
import numpy as np
import utils
import re


from CommandLineInterface import CLI


class SIFplot:
    @staticmethod
    def single(paths: list[str], window:str = 'full', reduce_noise:bool = False):
        plt.figure()
        for path in paths:
            data, _ = utils.parse(path)

            data = utils.slice_window(data, window=window)

            wavelengths, counts = data[:, 0], data[:, 1]

            if reduce_noise:
                wavelengths, counts = utils.gradient_n_sigma(wavelengths, counts)

            filename = os.path.basename(path)
            plt.plot(wavelengths, counts, label=filename)
        plt.legend(fontsize='small')  # Decrease the font size of the legend
        plt.xlabel("Wavelength")
        plt.ylabel("Counts")
        plt.show()
        

    @staticmethod
    def batch(paths: list[str], window:str = 'full', reduce_noise:bool = False):
        for path in paths:
            data, _ = utils.parse(path)
            wavelengths, counts = data[:, 0], data[:, 1]
            data = utils.slice_window(data, window=window)
            wavelengths, counts = data[:, 0], data[:, 1]
            if reduce_noise:
                wavelengths, counts = utils.gradient_n_sigma(wavelengths, counts)
            filename = os.path.basename(path)
            plt.figure()
            plt.plot(wavelengths, counts, label=filename)
            plt.legend(fontsize='small')  # Decrease the font size of the legend
            plt.xlabel("Wavelength")
            plt.ylabel("Counts")
            plt.title(f"Plot of {filename}")
            plt.show()

    @staticmethod
    def hyperspectrum(directory: list[str], window:str = 'SHG', reduce_noise:bool = False, colorscheme:str = 'Blues'):
        
        def extract_positions(files):
            # Regular expression pattern to match the image number and coordinates
            pattern = re.compile(r'_(\d+)_([0-9.]+)_([0-9.]+)_')
            # Extract the information
            extracted_params = [pattern.search(file).groups() for file in files]
            return extracted_params
    
        def normalize_array(array):
            array_min = np.min(array)
            array_max = np.max(array)
            
            # Avoid division by zero in case the array is constant
            if array_max - array_min == 0:
                return np.zeros_like(array)
            
            normalized_array = (array - array_min) / (array_max - array_min)
            return normalized_array

        if os.path.isfile(directory[0]):
            print("Please dump entire folder instead.")
            return
        else:
            files = utils.extract_files_from_folder(directory)

        background_file = CLI.menu_select(files)
        files.remove(background_file)
        
        # Extract positions and sort files based on positions
        positions = extract_positions(files)

        # Parse and process the background file
        background_data, _ = utils.parse(os.path.join(directory[0], background_file))
        background_data = utils.slice_window(background_data, window=window)
        bg_wavelengths, bg_counts = background_data[:, 0], background_data[:, 1]

        if reduce_noise:
            bg_wavelengths, bg_counts = utils.gradient_n_sigma(bg_wavelengths, bg_counts)
        
        pixels = []
        for file in files:
            print(file)
            data, _ = utils.parse(os.path.join(directory[0], file))

            data = utils.slice_window(data, window=window)
            wavelengths, counts = data[:, 0], data[:, 1]

            if reduce_noise:
                wavelengths, counts = utils.gradient_n_sigma(wavelengths, counts)
            
            # Interpolate background counts to match the wavelengths of the current data
            bg_interp = interp1d(bg_wavelengths, bg_counts, kind='linear', bounds_error=False, fill_value=0)
            bg_counts_interpolated = bg_interp(wavelengths)

            # Ensure counts do not go below zero after background subtraction
            adjusted_counts = np.maximum(counts - bg_counts_interpolated, 0)
            
            pixels.append(int(np.sum(adjusted_counts)))
        
        normalized_pixels = normalize_array(np.array(pixels))
    

        # Create a dictionary to hold the pixel values by position
        counts_by_position = {(float(pos[1]), float(pos[2])): normalized_pixels for pos, normalized_pixels in zip(positions, normalized_pixels)}

        # Determine the grid size
        max_x = int(max(float(pos[1]) for pos in positions)) + 1
        max_y = int(max(float(pos[2]) for pos in positions)) + 1
        heatmap_data = np.zeros((max_y, max_x))

        # Fill the heatmap data based on the positions
        for pos, count in counts_by_position.items():
            x, y = int(pos[0]), int(pos[1])
            heatmap_data[y, x] = count

        # Plot the heatmap
        plt.figure(figsize=(10, 10))
        plt.imshow(heatmap_data, cmap=colorscheme, aspect='auto')
        plt.colorbar(label='Summed Counts')
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Heatmap of Hyperspectral Data')
        plt.show()


    
    @staticmethod
    def sif2array(paths: list[str], loc: str):
        if not os.path.exists(loc):
            print('Files could not be saved: Location does not exist.')
            return
            
        for i, path in enumerate(paths):
            data, _ = utils.parse(path)
            file_name = os.path.join(loc, f"arr{i+1}.csv")
            np.savetxt(file_name, data, delimiter=",", header="Wavelength,Counts", comments='')
            print(f"Array for {path} saved to {file_name}")