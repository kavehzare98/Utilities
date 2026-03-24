# Utilities
Repo where I keep all the utilities I write for myself.

## Current Utilities

1. Line Copy (`lin_cpy.py`)
    - This utility copies specified lines of text from file into clipboard.
    - By default, the tool finds the latest edited file in the current directory.
    - User can also specify a file (or filepath) to copy from.
2. TBD...

## Key Assumptions

1. I'm using Ubuntu Linux, hence, I'm sure these utilities won't work on Windows and may fail on Mac.
2. I've pre-installed `xclip` for copying text into clipboard directly from terminal.
3. I have Python version `3.13+` already installed on my system.

## Set Up
```bash
# Change Permissions for Utility
chmod +x lin_cpy.py

# Find PATH variable
echo $PATH

# Move executable to one of the PATH directories (with root privilege)
sudo mv lin_cpy.py <path>/lin_cpy
```

## Usage

```bash
# To get detailed instructions
lin_cpy -h (or --help, -help, --h)

# Example 1:
lin_cpy

# Example 2:
lin_cpy <file_name>
```
