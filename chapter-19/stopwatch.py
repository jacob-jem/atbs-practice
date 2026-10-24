"""A simple stopwatch that records lap times and copies them to the clipboard.

Usage: python3 stopwatch.py

Press ENTER to start the stopwatch, and then press ENTER again to mark each lap.
Each lap is printed with its lap number, the total time elapsed, and the time
for that lap, in seconds. Press Ctrl-C to stop, and the lap times are copied to
the clipboard. If no laps were marked, the clipboard is left unchanged.

Requires pyperclip (pip3 install pyperclip).
"""

import time, pyperclip


def main():

    # Display the program's instructions.
    print("Press ENTER to begin and to mark laps. Ctrl-C quits.")

    # Initialize an empty string to store the lap times for copying to the clipboard later.
    text = ""

    # Start the stopwatch and track the lap times until the user presses Ctrl-C.
    try:
        input()  # Press Enter to begin.
        print("Started.")
        start_time = time.monotonic()  # Get the first lap's start time.
        last_time = start_time  # Set initial last lap time as the start time.
        lap_number = 1  # Track the lap number starting from 1.

        while True:
            # Wait for the user to press Enter.
            input()

            # Get the current time once, so the lap time and total time are measured from the same moment.
            now = time.monotonic()
            lap_time = now - last_time
            total_time = now - start_time

            # Print the lap number, total time, and lap time, and add the same line to the text for the clipboard.
            lap_line = f"Lap #{lap_number:2}: {total_time:6.2f} ({lap_time:6.2f})"
            print(lap_line)
            text += lap_line + "\n"

            # Increment the lap number and reset the last lap time.
            lap_number += 1
            last_time = now

    # Handle Ctrl-C (and Ctrl-D, which ends the input) to keep the error message from displaying.
    except (KeyboardInterrupt, EOFError):
        print("\nDone.")

    # Copy the lap times to the clipboard, if any laps were marked.
    if text:
        try:
            pyperclip.copy(text)
        except pyperclip.PyperclipException:
            print("Could not copy the lap times to the clipboard.")


if __name__ == "__main__":
    main()
