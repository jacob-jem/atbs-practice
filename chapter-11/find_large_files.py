"""List folders and files that are larger than 100 MB.

Usage: python3 find_large_files.py <folder>

Walks through the folder and its subfolders. Prints the path of every folder
whose total size (including its subfolders) exceeds 100 MB, and the path of
every individual file that exceeds 100 MB. Nothing is deleted.
"""

import os
from pathlib import Path
import sys

# 100 MB in bytes (1 MB = 1024 * 1024 bytes).
SIZE_LIMIT = 100 * 1024 * 1024


def main():

    # Check if the correct number of command line arguments is provided.
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 find_large_files.py <folder>")

    # Get the folder path from command line arguments, and make sure it exists.
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}")

    # Walk through the folder and its subfolders.
    for current_folder, _, filenames in os.walk(folder):
        current_folder = Path(current_folder)

        # If the folder's total size exceeds the limit, print the folder path.
        if get_folder_size(current_folder) > SIZE_LIMIT:
            print(current_folder)

        # If an individual file exceeds the limit, print the file path.
        for filename in filenames:
            if get_file_size(current_folder / filename) > SIZE_LIMIT:
                print(current_folder / filename)


def get_file_size(file):
    """Return the size of a file in bytes, or 0 if it can't be determined (e.g. a broken link)."""
    try:
        return os.path.getsize(file)
    except OSError:
        return 0


def get_folder_size(folder):
    """Return the total size in bytes of all files in a folder and its subfolders."""

    size = 0

    # Walk through the folder and its subfolders.
    for current_folder, _, filenames in os.walk(folder):
        current_folder = Path(current_folder)

        # Add up the size of every file.
        for filename in filenames:
            size += get_file_size(current_folder / filename)

    return size


if __name__ == "__main__":
    main()
