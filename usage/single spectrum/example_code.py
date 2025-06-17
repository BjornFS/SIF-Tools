from sif_tools import SIFconvert
import matplotlib.pyplot as plt
import seaborn as sns

# Use seaborn's style
sns.set_theme(style="whitegrid", context="notebook", palette="deep")

file = "tests/UnitTest.sif"

data = SIFconvert(file)
wavelength, count = data[:, 0], data[:, 1]

plt.figure(figsize=(10, 6), dpi=120)

# Plot with seaborn lineplot for better aesthetics
sns.lineplot(x=wavelength, y=count, linewidth=2.5)

# Labels and title
plt.xlabel("Wavelength (nm)", fontsize=14)
plt.ylabel("Count", fontsize=14)
plt.title("Spectrum from SIF file", fontsize=16, weight='bold')

# Tight grid and nicer layout
plt.grid(True, which='major', linestyle='--', linewidth=0.5)
plt.tight_layout()

plt.show()