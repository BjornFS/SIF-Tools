from sif_tools import hyperspectrum
import matplotlib.pyplot as plt

dir = '/path/to/directory/'
bg  = '/path/to/directory/bg.sif' 

data = hyperspectrum(directory = dir, background = bg, reduce_noise=True, window='pinched')

# Plot the heatmap
plt.figure(figsize=(10, 10))
plt.imshow(data, cmap='Blues', aspect='auto')
plt.colorbar(label='Summed Counts')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.title('Heatmap of Hyperspectral Data')
plt.show()