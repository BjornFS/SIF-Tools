from sif_tools import sif2array

import matplotlib.pyplot as plt
import os

files = ['folder/file1.sif', 'folder/file2.sif']

       
plt.figure() # initialise plot

data_collection = [] # initialise list to store multiple images

for file in files:
    data = sif2array(target=file, reduce_noise=True, window='reduced')
    wavelengths, counts = data[:, 0], data[:, 1] # separate wavelengths and count from 'data'

    filename = os.path.basename(file) # use filename as legend
    plt.plot(data, counts, label=filename)

plt.legend(fontsize='small')
plt.xlabel("Wavelength")
plt.ylabel("Counts")
plt.show()