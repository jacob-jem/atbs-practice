"""Close the gaps in a sequence of numbered files.

Usage: python3 renumbering_files.py <folder> <prefix>

Looks in the folder and each of its subfolders for files named like
<prefix><number>.<extension> (for example spam001.txt). Each folder is
handled separately. The files are renamed so their numbers run 1, 2, 3, ...
with no gaps, in the same order as before. The original zero padding is kept.

Example: with spam1.txt, spam2.txt and spam4.txt, spam4.txt becomes spam3.txt.
Files that share a number but have different extensions (spam2.txt and
spam2.png) are treated as one item and get the same new number.
"""

import os, re, shutil
from pathlib import Path
import sys


def main():

    # Check if the correct number of command line arguments is provided.
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 renumbering_files.py <folder> <prefix>")

    # Get the folder path and prefix from command line arguments.
    folder = Path(sys.argv[1])
    prefix = sys.argv[2]

    # Make sure the folder exists.
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}")

    # Match whole filenames like <prefix><number>.<extension>.
    # re.escape makes sure special characters in the prefix are matched literally.
    pattern = re.compile(rf"{re.escape(prefix)}(\d+)(\..+)")

    # Walk through the folder and its subfolders.
    for current_folder, _, filenames in os.walk(folder):
        current_folder = Path(current_folder)

        # Collect the numbered files as (number, digit count, extension, filename).
        numbered_files = []
        for filename in filenames:
            if match := pattern.fullmatch(filename):
                digits, extension = match.groups()
                numbered_files.append((int(digits), len(digits), extension, filename))

        # Map each existing number to its new number: 1, 2, 3, ... in the same order.
        old_numbers = sorted({number for number, _, _, _ in numbered_files})
        new_numbers = {old: new for new, old in enumerate(old_numbers, start=1)}

        # Rename from the lowest number up, so no file is overwritten.
        for number, digit_count, extension, filename in sorted(numbered_files):
            new_number = str(new_numbers[number]).zfill(digit_count)
            new_filename = f"{prefix}{new_number}{extension}"

            # Skip files that are already numbered correctly.
            if new_filename == filename:
                continue

            shutil.move(current_folder / filename, current_folder / new_filename)
            print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    main()
