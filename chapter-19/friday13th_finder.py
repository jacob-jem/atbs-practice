"""Print the next 10 Friday the 13ths and all of the previous Friday the 13ths.

Usage: python3 friday13th_finder.py

The program takes no command line arguments. It uses the datetime module and
checks each day, starting from today, going forward until it has found 10
Friday the 13ths, and then going backward until it reaches the year 1. Today is
checked in both directions, so if today is a Friday the 13th, it appears in both
lists. Each one is printed as its month and year, with the closest to today first.
"""

from datetime import date, timedelta

# The weekday number of Friday, where Monday is 0 (as used by date.weekday()).
FRIDAY = 4


def main():

    # Print the next 10 Friday the 13ths and the previous Friday the 13ths, both counting today.
    print(f"The next 10 Friday the 13ths, counting today, will be in:\n{find_future()}")
    print(f"The previous Friday the 13ths, counting today, were in:\n{find_past()}")


def find_future():
    """Return a string with the month and year of the next 10 Friday the 13ths, starting from today."""

    # Initialize an empty string to store the results, a counter for the number of Friday the 13ths found,
    # and set the starting day to today.
    text = ''
    friday13th_counter = 0
    day = date.today()
    one_day = timedelta(days=1)

    # Loop through the days starting from today going forward, checking if each day is a Friday the 13th,
    # and appending the month and year to the text string until 10 Friday the 13ths are found.
    while friday13th_counter < 10:
        if day.day == 13 and day.weekday() == FRIDAY:  # Check if it's Friday the 13th.
            text += day.strftime("%B, %Y\n")  # Append the month and year to the text.
            friday13th_counter += 1
        day += one_day

    # Return the text string containing the next 10 Friday the 13ths.
    return text


def find_past():
    """Return a string with the month and year of every previous Friday the 13th, starting from today."""

    # Initialize an empty string to store the results, set the starting day to today,
    # and create a timedelta object representing one day.
    text = ''
    day = date.today()
    one_day = timedelta(days=1)

    # Loop through the days starting from today going backward, checking if each day is a Friday the 13th,
    # and appending the month and year to the text string until the minimum date is reached.
    while True:
        if day.day == 13 and day.weekday() == FRIDAY:  # Check if it's Friday the 13th.

            # Use day.year instead of %Y, because %Y does not format years before 1000 the same way on every system.
            text += day.strftime(f"%B, {day.year}\n")  # Append the month and year to the text.

        if day == date.min:  # Stop if we reach the minimum date.
            break

        day -= one_day  # Move to the previous day.

    # Return the text string containing the previous Friday the 13ths.
    return text


if __name__ == "__main__":
    main()
