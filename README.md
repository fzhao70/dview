# dview - Scientific Data File Viewer

A command line tool to quickly inspect scientific data file formats.

## Installation

```bash
python build.py
```

## Usage

Basic usage:
```bash
# View header information
dview data.npy

# View header and all data
dview -a data.npy

# View multiple files
dview data.h5 data.nc data.npy
```

### Supported File Formats

- NumPy arrays (.npy)
- NumPy compressed arrays (.npz)
- HDF5 files (.h5, .hdf5)
- NetCDF files (.nc, .netcdf)
- Matlab files (.mat) Only support v4 (Level 1.0), v6 and v7 to 7.2 matfiles


### Command Line Options

```
dview [-h] [-a] [-v] files [files ...]

positional arguments:
  files            One or more files to inspect

optional arguments:
  -h, --help      Show this help message and exit
  -a, --all       Show all data in addition to header information
  -v, --version   Show program's version number and exit
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
