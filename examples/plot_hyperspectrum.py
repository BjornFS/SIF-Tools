# Now you can import sif2array
from sif_tools import hyperspectrum
import matplotlib.pyplot as plt

bg = 'BG_1s_150l.sif'
directory = 'tests/PL_mapping240603/'

data = hyperspectrum(directory = directory, background = bg, size = (5,5), reduce_noise=True, window='pinched')

# Plot the heatmap
plt.figure(figsize=(10, 10))
plt.imshow(data, cmap='Blues', aspect='auto')
plt.colorbar(label='Normalised Counts')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Heatmap of Hyperspectral Data')
plt.show()