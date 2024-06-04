from sif_tools import sif2array

file = 'UnitTests/UnitTest files/test_1.sif'

data = sif2array(target=file, reduce_noise=True, window='reduced')
wavelengths, counts = data[:, 0], data[:, 1] # separate wavelengths and count from 'data'

print(wavelengths, counts)