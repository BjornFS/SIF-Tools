from sif_tools import sif2array

import matplotlib.pyplot as plt

# Update the file path to point to the test_1.sif file in UnitTests/UnitTest files
files = ['UnitTests/UnitTest files/test_1.sif', 'UnitTests/UnitTest files/test_2.sif']

plt.figure()
for file in files:
    data = sif2array(target=file, reduce_noise=True, window='reduced')
    wavelengths, counts = data[:, 0], data[:, 1] # separate wavelengths and count from 'data'
    plt.plot(wavelengths, counts)  # plot wavelengths vs counts
plt.xlabel("Wavelength")
plt.ylabel("Counts")
plt.title("Spectrum")
plt.show()