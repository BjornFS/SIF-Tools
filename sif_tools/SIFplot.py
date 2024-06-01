import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import os
import numpy as np

from .utils import MATH, FILE
from CommandLine.CommandLineInterface import CLI


class SIFplot:
    @staticmethod
    def single(paths: list[str], window:str = 'full', reduce_noise:bool = False):

        if os.path.isfile(paths[0]):
            pass
        else:
            paths = FILE.extract_files_from_folder(paths[0])
            
        plt.figure()
        for path in paths:
            data, _ = FILE.parse(path)

            data = MATH.slice_window(data, window=window)

            wavelengths, counts = data[:, 0], data[:, 1]

            if reduce_noise:
                wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)

            filename = os.path.basename(path)
            plt.plot(wavelengths, counts, label=filename)
        plt.legend(fontsize='small')  # Decrease the font size of the legend
        plt.xlabel("Wavelength")
        plt.ylabel("Counts")
        plt.show()

        return
        

    @staticmethod
    def batch(paths: list[str], window:str = 'full', reduce_noise:bool = False):
        
        if os.path.isfile(paths[0]):
            pass
        else:
            paths = FILE.extract_files_from_folder(paths[0])

        for path in paths:
            data, _ = FILE.parse(path)
            wavelengths, counts = data[:, 0], data[:, 1]
            data = MATH.slice_window(data, window=window)
            wavelengths, counts = data[:, 0], data[:, 1]
            if reduce_noise:
                wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)
            filename = os.path.basename(path)
            plt.figure()
            plt.plot(wavelengths, counts, label=filename)
            plt.legend(fontsize='small')  # Decrease the font size of the legend
            plt.xlabel("Wavelength")
            plt.ylabel("Counts")
            plt.title(f"Plot of {filename}")
            plt.show()

        return

    @staticmethod
    def hyperspectrum(directory: list[str], window:str = 'SHG', reduce_noise:bool = False, colorscheme:str = 'Blues'):

        if os.path.isfile(directory[0]):
            print("Please dump entire folder, not individual files.")
            return
        else:
            files = FILE.extract_files_from_folder(directory[0])

        background_file = CLI.menu_select(files)
        files.remove(background_file)
        
        # Extract positions and sort files based on positions
        positions = FILE.extract_positions(files)

        # Parse and process the background file
        background_data, _ = FILE.parse(os.path.join(directory[0], background_file))
        background_data = MATH.slice_window(background_data, window=window)
        bg_wavelengths, bg_counts = background_data[:, 0], background_data[:, 1]

        if reduce_noise:
            bg_wavelengths, bg_counts = MATH.gradient_n_sigma(bg_wavelengths, bg_counts)
        
        pixels = []
        for file in files:
            data, _ = FILE.parse(os.path.join(directory[0], file))

            data = MATH.slice_window(data, window=window)
            wavelengths, counts = data[:, 0], data[:, 1]

            if reduce_noise:
                wavelengths, counts = MATH.gradient_n_sigma(wavelengths, counts)
            
            # Interpolate background counts to match the wavelengths of the current data
            bg_interp = interp1d(bg_wavelengths, bg_counts, kind='linear', bounds_error=False, fill_value=0)
            bg_counts_interpolated = bg_interp(wavelengths)

            # Ensure counts do not go below zero after background subtraction
            adjusted_counts = np.maximum(counts - bg_counts_interpolated, 0)
            
            pixels.append(int(np.sum(adjusted_counts)))
        
        normalized_pixels = MATH.normalize_array(np.array(pixels))
    

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

        return

    
    @staticmethod
    def sif2csv(paths: list[str], loc: str):
        if not os.path.exists(loc):
            print('Files could not be saved: Location does not exist.')
            return
        
        if os.path.isfile(paths[0]):
            pass
        else:
            paths = FILE.extract_files_from_folder(paths[0])
            
        for i, path in enumerate(paths):
            print(path)
            data, _ = FILE.parse(path)
            # Get the base filename without extension and add .csv
            file_name = os.path.splitext(os.path.basename(path))[0] + ".csv"
            # Combine with the location path
            file_name = os.path.join(loc, file_name)
            np.savetxt(file_name, data, delimiter=",", header="Wavelength,Counts", comments='')

        return