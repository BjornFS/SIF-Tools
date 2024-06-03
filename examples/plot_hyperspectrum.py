from sif_tools import hyperspectrum
import matplotlib.pyplot as plt

bg = 'UnitTests/UnitTest files/test_background.sif'
directory = 'UnitTests/UnitTest files/'

data = hyperspectrum(directory = directory, background = bg, size = (4,4), reduce_noise=True, window='pinched')

# Plot the heatmap
plt.figure(figsize=(10, 10))
plt.imshow(data, cmap='Blues', aspect='auto')
plt.colorbar(label='Normalised Counts')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Heatmap of Hyperspectral Data')
plt.show()