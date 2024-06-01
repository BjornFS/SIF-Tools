# SIF-Toolkit

SIF-Toolkit is an extremely light-weight Python toolkit designed to read `.sif` data files from an Andor Solis spectrometer. This toolkit includes a set of utilities for opening, analyzing, and plotting data from `.sif` files, providing a convenient way to handle spectrometer data in scientific workflows.

This Toolkit is borrows, and is adapted, from [sif_parser](https://github.com/fujiisoup/sif_parser) by [fujiisoup](https://github.com/fujiisoup). 

## Features

- **Read .sif files:** Efficiently load and parse `.sif` files from Andor Solis spectrometers.
- **Data manipulation:** Tools for handling and processing spectrometer data.
- **Visualization:** Plot data directly from `.sif` files.

## Requirements

- Python >= 3.6
- NumPy
- Matplotlib

## Installation

```bash
git clone https://github.com/BjornFS/SIF-Toolkit.git
```

## Usage

### Importing SIF-Toolkit in a Python Script

A specific class ```SIFpy``` has been written for the purposes of in-script parsing.

It can be called in the following way
```python 
from SIFpy import sif2array
import os

file = os.path.abspath('/Users/user/location/file.sif')
data = sif2array(target=file, reduce_noise=False, window='narrow').get_data()
```

### Running SIF-Toolkit from the Command Line

A client has been included, consisting of ```CommandLineInterface``` & ```CommandLineTools```, which is run from ```__main__.py``` 

```bash
python3 dir/SIF-Toolkit
```

This will execute the default command-line interface, providing a quick way to process and visualize your `.sif` data.

Once booted, the user will be met with:

```
                    _            _____                         
    /\             | |          |  __ \                        
   /  \   _ __   __| | ___  _ __| |__) |_ _ _ __ ___  ___ _ __ 
  / /\ \ | '_ \ / _` |/ _ \| '__|  ___/ _` | '__/ __|/ _ \ '__|
 / ____ \| | | | (_| | (_) | |  | |  | (_| | |  \__ \  __/ |   
/_/    \_\_| |_|\__,_|\___/|_|  |_|   \__,_|_|  |___/\___|_|   
                                                               

This software is released under MPL-2.0
May 2024        Version 1.1
Author: Bjørn Funch Schrøder Nielsen @ bjornfschroder@gmail.com

--- A program to read and plot Andor Technology Multi-Channel files (.sif) ---

Available commands:
[help]          -help
[plot]          -plot
[batchjob]      -batch
[hyperspectrum] -hyperspectrum
[sif-2-csv]     -convert


>>> _
```

## Command Line Interface

SIF-Toolkit includes several command-line tools for specific tasks. The files themselves can be explicitly written, or drag-and-dropped into the command line. Here are a few examples:

- **Create a single plot, using one or more files:**

```bash
-plot -window = narrow -reduce_noise /Users/user/location/file.sif
```

- **Plot as individual plots, using one or more files**

```bash
-batch -window = narrow -reduce_noise /Users/user/location/file.sif
```

- **Plot 2D heatmap of collection of files:**
```bash
-hyperspectrum -window = narrow -reduce_noise /Users/user/folder/
```

etc.

## Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/SIF-Toolkit/issues).

## Contributing

We welcome contributions! Please fork the repository and submit pull requests.

## Authors

- Bjorn Schroder, Technical University of Denmark
- Bjornfschroder@gmail.com
