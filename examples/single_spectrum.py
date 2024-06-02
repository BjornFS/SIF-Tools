from sif_tools import sif2array

import matplotlib.pyplot as plt

file = 'folder/file1.sif'

data = sif2array(target=file, reduce_noise=True, window='reduced')
wavelengths, counts = data[:, 0], data[:, 1] # separate wavelengths and count from 'data'

plt.figure() # initialise plot
plt.xlabel("Wavelength")
plt.ylabel("Counts")
plt.show()