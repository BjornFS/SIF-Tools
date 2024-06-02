from sif_tools import sif2array

file = 'folder/file.sif'
data = sif2array(target=file, reduce_noise=True, window='narrow')

print(data)
