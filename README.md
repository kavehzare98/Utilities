# Utilities
Repo where I keep all the little utilities I write for myself.

## Current Utilities

1. Line Copy (`lin_cpy.py`)
    - This utility copies specified lines of text from file.
    - By default, the tool finds the latest edited file in the current directory.
    - User can also specify a file (or filepath) to copy from.
2. TBD...

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
