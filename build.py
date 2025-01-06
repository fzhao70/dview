# build.py
import os
import shutil
import subprocess
import sys

def build_binary():
    """Build the binary using PyInstaller"""
    try:

        # Install required packages
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install',
            'pyinstaller',
            'numpy',
            'h5py',
            'netCDF4',
            'scipy'
        ])

        # Build the binary
        subprocess.check_call(['pyinstaller', 'dview.spec', '--clean'])

        # Move the binary to current directory
        shutil.copy('dist/dview', 'dview')
        
        # Clean up build files
        for dir_name in ['build', 'dist', '__pycache__']:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
        
         
        print("\nBuild successful! The 'dview' binary has been created.")
        print("You can now use it by running: ./dview filename")
        print("\nExample usage:")
        print("  ./dview data.npy             # Show header only")
        print("  ./dview -a data.npy          # Show header and all data")
        print("  ./dview data.h5 data.nc      # Multiple files")
        
        
    except Exception as e:
        print(f"Error during build: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    build_binary()
