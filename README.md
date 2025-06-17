# SIF-Tools

SIF-Tools is a light-weight Python toolkit designed to read `.sif` data files from an Andor Solis spectrometer, and convert them into easy-to-access numpy arrays.

## Requirements

- Python >= 3.6
- NumPy

## Installation

* Pip install
```bash
pip install sif-toolkit
```

* Clone the repository
```bash
git clone https://github.com/BjornFS/SIF-Toolkit.git
```

## Usage

### Importing SIF-Tools in a Python Script

```python 
from sif_tools import SIFconvert

data = SIFconvert('tests/UnitTest.sif')
wavelength, count = data[:, 0], data[:, 1]
```

![Spectrum]("usage/single spectrum/example_plot.png")

## Support

If you encounter any issues, have suggestions for add-ons, or have questions, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/SIF-Toolkit/issues).

## Authors

- Bjorn Schroder Nielsen
- Bjorn@SchroderNielsen.com
