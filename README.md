# SIF-Toolkit

SIF-Toolkit is a Python toolkit designed to read `.sif` data files from an Andor Solis spectrometer. This toolkit includes a set of utilities for opening, analyzing, and plotting data from `.sif` files, providing a convenient way to handle spectrometer data in your scientific workflows.

## Features

- **Read .sif files:** Efficiently load and parse `.sif` files from Andor Solis spectrometers.
- **Data manipulation:** Tools for handling and processing spectrometer data.
- **Visualization:** Plot data directly from `.sif` files.

## Requirements

- Python 3.x
- NumPy
- Matplotlib

## Installation

You can clone the repository and install it manually:

```bash
git clone https://github.com/yourusername/SIF-Toolkit.git
```

## Usage

### Importing SIF-Toolkit in a Python Script

```python
from SIFopen import SIFFile
from SIFplot import plot_sif_data
import utils

# Load a .sif file
sif_file = SIFFile('path_to_your_file.sif')

# Access data
data = sif_file.get_data()

# Process data (example: normalize)
normalized_data = utils.normalize(data)

# Plot data
plot_sif_data(normalized_data)
```

### Running SIF-Toolkit from the Command Line

```bash
python CommandLineInterface.py path_to_your_file.sif
```

This will execute the default command-line interface, providing a quick way to process and visualize your `.sif` data.

## Command Line Tools

SIF-Toolkit includes several command-line tools for specific tasks. Here are a few examples:

- **Open a .sif file and print metadata:**

```bash
python CommandLineTools.py open path_to_your_file.sif
```

- **Plot data from a .sif file:**

```bash
python CommandLineTools.py plot path_to_your_file.sif
```

## Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/SIF-Toolkit/issues).

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

## Authors

- Bjorn Schroder, Technical University of Denmark
- Bjornfschroder@gmail.com
