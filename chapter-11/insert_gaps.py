"""Insert a gap in a sequence of numbered files.

Usage: python3 insert_gaps.py <folder> <prefix> <insert_number>

Looks in the folder and each of its subfolders for files named like
<prefix><number>.<extension> (for example spam001.txt). Each folder is
handled separately. Every file numbered <insert_number> or higher is renamed
to the next number up, which leaves a gap at <insert_number>. The original
zero padding is kept.

Example: with spam1.txt, spam2.txt and spam3.txt and an insert number of 2,
spam3.txt becomes spam4.txt and spam2.txt becomes spam3.txt, so no file is
left at spam2.txt.
"""

import os, re, shutil
from pathlib import Path
import sys


def main():

    # Check if the correct number of command line arguments is provided.
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 insert_gaps.py <folder> <prefix> <insert_number>")

    # Get the folder path, prefix, and insert number from command line arguments.
    folder = Path(sys.argv[1])
    prefix = sys.argv[2]
    try:
        insert_number = int(sys.argv[3])
    except ValueError:
        sys.exit("The insert number must be a whole number.")

    # Make sure the folder exists.
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}")

    # Match whole filenames like <prefix><number>.<extension>.
    # re.escape makes sure special characters in the prefix are matched literally.
    pattern = re.compile(rf"{re.escape(prefix)}(\d+)(\..+)")

    # Walk through the folder and its subfolders.
    for current_folder, _, filenames in os.walk(folder):
        current_folder = Path(current_folder)

        # Collect the numbered files in this folder as:
        # (number, digit count, extension, filename).
        numbered_files = []
        for filename in filenames:
            if match := pattern.fullmatch(filename):
                digits, extension = match.groups()
                numbered_files.append((int(digits), len(digits), extension, filename))

        # Rename from the highest number down, so no file is overwritten.
        for number, digit_count, extension, filename in sorted(numbered_files, reverse=True):
            if number >= insert_number:
                new_number = str(number + 1).zfill(digit_count)
                new_filename = f"{prefix}{new_number}{extension}"
                shutil.move(current_folder / filename, current_folder / new_filename)
                print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    main()
