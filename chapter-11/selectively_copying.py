"""Copy all .pdf and .jpg files from one folder tree to another.

Usage: python3 selectively_copying.py <source_folder> <destination_folder>

Walks through the source folder and its subfolders. Every file ending in
.pdf or .jpg (in any capitalization, such as .PDF or .JPG) is copied to the
destination folder, keeping the same folder structure as in the source.
Files already in the destination with the same name are overwritten. The
source files are not changed.
"""

import os, shutil
from pathlib import Path
import sys

# The file extensions to copy, in lowercase.
EXTENSIONS = {".pdf", ".jpg"}


def main():

    # Check if the correct number of command line arguments is provided.
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 selectively_copying.py <source_folder> <destination_folder>")

    # Get the source and destination folder paths from command line arguments.
    source = Path(sys.argv[1])
    destination = Path(sys.argv[2])

    # Make sure the source exists, and that the destination isn't inside it
    # (otherwise the program would end up copying its own copies).
    if not source.is_dir():
        sys.exit(f"Source folder not found: {source}")
    if destination.resolve().is_relative_to(source.resolve()):
        sys.exit("The destination folder can't be inside the source folder.")

    # Walk through each folder and its subfolders in the source directory.
    for current_folder, _, filenames in os.walk(source):
        current_folder = Path(current_folder)

        for filename in filenames:
            file_path = current_folder / filename

            # Copy the file if it's a pdf or jpg, recreating its subfolder in the destination.
            if file_path.suffix.lower() in EXTENSIONS:
                target_folder = destination / current_folder.relative_to(source)
                target_folder.mkdir(parents=True, exist_ok=True)
                new_file = target_folder / filename
                shutil.copy(file_path, new_file)
                print(f"Copied: {file_path} -> {new_file}")


if __name__ == "__main__":
    main()
