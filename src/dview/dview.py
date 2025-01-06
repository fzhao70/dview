#!/usr/bin/env python3
import numpy as np
import h5py
import netCDF4 as nc
import argparse
import sys
import scipy.io as sio
from pathlib import Path

def inspect_mat(file_path, show_all=False):
    """
    Inspect a MATLAB .mat file and print its structure and optionally all data.
    Only support v4 (Level 1.0), v6 and v7 to 7.2 matfiles

    Args:
        file_path (str): Path to the .mat file
        show_all (bool): Whether to print all data
    """
    try:
        data = sio.loadmat(file_path)
        print(f"\nFile: {file_path}")
        print("Format: MATLAB < v7.3")
        print("\nVariables:")
        print("-" * 50)

        # Filter out special variables that start with '__'
        variables = {k: v for k, v in data.items() if not k.startswith('__')}

        for var_name, var_data in variables.items():
            print(f"Variable: {var_name}")
            print(f"  Type: {var_data.dtype}")
            print(f"  Shape: {var_data.shape}")
            if show_all:
                print("  Data:")
                print(var_data)
            print()

    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)


def inspect_npy(file_path:str, show_all=False):
    """
    Inspect a .npy file and print its dimensions and optionally all data.

    Args:
        file_path (str): Path to the .npy file
        show_all (bool): Whether to print all data
    """
    try:
        data = np.load(file_path)
        print(f"\nFile: {file_path}")
        print(f"Type: {data.dtype}")
        print(f"Shape: {data.shape}")
        print(f"Dimensions: {data.ndim}")

        if show_all:
            print("\nData:")
            print("-" * 50)
            print(data)
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def inspect_npz(file_path:str, show_all=False):
    """
    Inspect a .npz file and print variable names, dimensions, and optionally all data.

    Args:
        file_path (str): Path to the .npz file
        show_all (bool): Whether to print all data
    """
    try:
        with np.load(file_path) as data:
            print(f"\nFile: {file_path}")
            print("\nVariables:")
            print("-" * 50)
            print(f"{'Name':<20} {'Type':<15} {'Shape':<20} {'Dimensions'}")
            print("-" * 50)

            for name in data.files:
                arr = data[name]
                print(f"{name:<20} {str(arr.dtype):<15} {str(arr.shape):<20} {arr.ndim}")

                if show_all:
                    print(f"\nData for {name}:")
                    print("-" * 50)
                    print(arr)
                    print()
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def inspect_netcdf(file_path:str, show_all=False):
    """
    Inspect a NetCDF file and print its structure and optionally all data.

    Args:
        file_path (str): Path to the NetCDF file
        show_all (bool): Whether to print all data
    """
    try:
        with nc.Dataset(file_path, 'r') as data:
            print(f"\nFile: {file_path}")

            # Print dimensions
            print("\nDimensions:")
            print("-" * 50)
            for dim_name, dim in data.dimensions.items():
                print(f"{dim_name}: {len(dim)} {'(unlimited)' if dim.isunlimited() else ''}")
            
            # Print variables
            print("\nVariables:")
            print("-" * 50)
            for var_name, var in data.variables.items():
                print(f"Name: {var_name}")
                print(f"  Type: {var.datatype}")
                print(f"  Dimensions: {var.dimensions}")
                print(f"  Shape: {var.shape}")
                print(f"  Attributes:")
                for attr_name in var.ncattrs():
                    print(f"    {attr_name}: {var.getncattr(attr_name)}")
                print()
                
                if show_all:
                    print(f"Data for {var_name}:")
                    print("-" * 50)
                    print(var[:])
                    print()
            
            # Print global attributes
            if data.ncattrs():
                print("\nGlobal Attributes:")
                print("-" * 50)
                for attr_name in data.ncattrs():
                    print(f"{attr_name}: {data.getncattr(attr_name)}")
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def inspect_hdf5(file_path:str, show_all=False):
    """
    Inspect an HDF5 file and print its structure and optionally all data.
    
    Args:
        file_path (str): Path to the HDF5 file
        show_all (bool): Whether to print all data
    """
    def print_attrs(name, obj):
        """Helper function to print attributes of HDF5 objects"""
        print(f"\n{name}:")
        print(f"  Type: {type(obj).__name__}")
        if isinstance(obj, h5py.Dataset):
            print(f"  Shape: {obj.shape}")
            print(f"  Dtype: {obj.dtype}")
        print("  Attributes:")
        for key, val in obj.attrs.items():
            print(f"    {key}: {val}")
        if show_all and isinstance(obj, h5py.Dataset):
            print("  Data:")
            print("-" * 50)
            print(obj[()])
            print()

    try:
        with h5py.File(file_path, 'r') as f:
            print(f"\nFile: {file_path}")
            print("\nFile Structure:")
            print("-" * 50)
            f.visititems(print_attrs)
    except Exception as e:
        print(f"Error reading {file_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Inspect various scientific data file formats (NumPy, NetCDF, HDF5)"
    )
    parser.add_argument(
        "files", 
        nargs="+", 
        help="One or more files to inspect"
    )
    parser.add_argument(
        "-a", "--all",
        action="store_true",
        help="Show all data in addition to header information"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    for file_path in args.files:
        path = Path(file_path)

        if not path.exists():
            print(f"Error: File {file_path} does not exist", file=sys.stderr)
            continue

        suffix = path.suffix.lower()
        if suffix == '.npy':
            inspect_npy(file_path, args.all)
        elif suffix == '.npz':
            inspect_npz(file_path, args.all)
        elif suffix in ['.nc', '.netcdf']:
            inspect_netcdf(file_path, args.all)
        elif suffix in ['.h5', '.hdf5']:
            inspect_hdf5(file_path, args.all)
        elif suffix == '.mat':
            inspect_mat(file_path, args.all)
        else:
            print(f"Error: Unsupported file format for {file_path}", file=sys.stderr)

if __name__ == "__main__":
    main()
