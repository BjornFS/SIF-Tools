from sif_tools import hyperspectrum
import matplotlib.pyplot as plt

bg = 'test_background.sif'
directory = 'UnitTests/UnitTest files'

data = hyperspectrum(directory = directory, 
                     background = bg, size = (4,4), 
                     reduce_noise=True, 
                     window='pinched', 
                     normalize=False)

# Plot the heatmap
plt.figure(figsize=(10, 10))
plt.imshow(data, cmap='Blues', aspect='auto')
plt.colorbar(label='Counts')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Hyperspectrum')
plt.show()