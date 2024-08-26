from sif_tools import sif2array
import numpy as np

file = 'UnitTests/UnitTest files/test_1.sif'

data = sif2array(target=file, reduce_noise=True, window='reduced')

#np.savetxt('test_1.csv', data, delimiter=",", header="Wavelength,Counts", comments='')
print(data)