"""Convert dates in filenames from MM-DD-YYYY to DD-MM-YYYY.

Usage: python3 converting_dates.py <folder>

Walks through the folder and its subfolders and renames any file whose name
contains a date in MM-DD-YYYY format. Files whose new name would already
exist are skipped, so nothing is overwritten.
"""

import os, re, shutil
from pathlib import Path
import sys


def main():

    # Check if the correct number of command line arguments is provided.
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 converting_dates.py <folder>")

    # Get the folder path from command line arguments, and make sure it exists.
    folder = Path(sys.argv[1])
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}")

    # Walk through the folder and its subfolders.
    for current_folder, _, filenames in os.walk(folder):
        current_folder = Path(current_folder)
        for filename in filenames:
            old_file = current_folder / filename

            # Find a date in the format MM-DD-YYYY that isn't part of a longer number.
            if match := re.search(r"(?<!\d)(\d{2})-(\d{2})-(\d{4})(?!\d)", filename):
                month, day, year = match.groups()

                # Only rename if the month and day are plausible.
                if 1 <= int(month) <= 12 and 1 <= int(day) <= 31:
                    new_filename = filename.replace(match.group(0), f"{day}-{month}-{year}")
                    new_file = current_folder / new_filename

                    # Skip files that wouldn't change (e.g. 05-05-2026).
                    if new_filename == filename:
                        continue

                    # Never overwrite an existing file.
                    if new_file.exists():
                        print(f"Skipped converting {filename}: {new_filename} already exists.")
                        continue

                    # Rename the old file to the new file name.
                    shutil.move(old_file, new_file)
                    print(f"Renamed: {filename} -> {new_filename}")


if __name__ == "__main__":
    main()
