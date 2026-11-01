# atbs-practice

Practice programs I wrote while working through *Automate the Boring Stuff
with Python* (3rd edition) by Al Sweigart. Each program is a solution to one
of the practice projects at the end of a chapter, organized into one folder per
chapter.

The programs were written for Python 3 and developed on macOS with Python 3.14.

## Programs

### Chapter 11: Organizing Files

| Program | What it does | Usage |
|---|---|---|
| [`selectively_copying.py`](chapter-11/selectively_copying.py) | Copies all `.pdf` and `.jpg` files from one folder tree to another, keeping the folder structure | `python3 selectively_copying.py <source_folder> <destination_folder>` |
| [`find_large_files.py`](chapter-11/find_large_files.py) | Lists folders and files larger than 100 MB | `python3 find_large_files.py <folder>` |
| [`renumbering_files.py`](chapter-11/renumbering_files.py) | Renames numbered files so the numbers run 1, 2, 3, ... with no gaps | `python3 renumbering_files.py <folder> <prefix>` |
| [`insert_gaps.py`](chapter-11/insert_gaps.py) | Renames numbered files to leave a gap at a chosen number | `python3 insert_gaps.py <folder> <prefix> <insert_number>` |
| [`converting_dates.py`](chapter-11/converting_dates.py) | Renames files so dates in the filename change from MM-DD-YYYY to DD-MM-YYYY | `python3 converting_dates.py <folder>` |

### Chapter 13: Web Scraping

| Program | What it does | Usage |
|---|---|---|
| [`2048.py`](chapter-13/2048.py) | Plays 2048 in Chrome by pressing random arrow keys until the game ends | `python3 2048.py` |
| [`link_verification.py`](chapter-13/link_verification.py) | Checks the links on a web page and reports the broken ones | `python3 link_verification.py <url>` |
| [`unsplash_downloader.py`](chapter-13/unsplash_downloader.py) | Downloads photos from Unsplash that match search keywords | `python3 unsplash_downloader.py -s <keyword> [<keyword> ...] [-n <number>]` |

### Chapter 19: Keeping Time, Scheduling Tasks, and Launching Programs

| Program | What it does | Usage |
|---|---|---|
| [`friday13th_finder.py`](chapter-19/friday13th_finder.py) | Prints the next 10 Friday the 13ths and all the previous ones | `python3 friday13th_finder.py` |
| [`stopwatch.py`](chapter-19/stopwatch.py) | A stopwatch that records lap times and copies them to the clipboard | `python3 stopwatch.py` |

Each program's docstring, at the top of its file, describes it in more detail.

## Setup

Install the third-party packages:

```
pip3 install -r requirements.txt
```

Some programs need more than that:

- `2048.py` and `unsplash_downloader.py` use Selenium and need Google Chrome installed.
- `link_verification.py` uses Playwright and needs its browser installed once:
  `playwright install chromium`
- The other programs use only Python's standard library, except `stopwatch.py`, which also needs `pyperclip`.

## Notes

- **Test on a copy first.** `converting_dates.py`, `renumbering_files.py` and
  `insert_gaps.py` rename files in place, and `selectively_copying.py`
  overwrites files with the same name in the destination folder. Try them on a
  copy of a folder before using them on files you care about.
- **The web programs can break.** `2048.py` and `unsplash_downloader.py` find
  page elements using the websites' current layout and CSS class names, so
  they may stop working if those sites change. Check a website's terms of use
  before running an automated program against it.
- `link_verification.py` does not follow a page's `<base href>` tag when it
  works out where relative links point.

## Credit

`stopwatch.py` is a modified version of the Project 14 stopwatch from [Automate the Boring Stuff with Python, 3rd edition](https://automatetheboringstuff.com/3e/) by Al Sweigart. The other programs are my own solutions to the book's practice projects.

## License

The code is licensed under the [MIT License](LICENSE), except `stopwatch.py`, which is licensed under [CC BY-NC-SA 4.0](LICENSE-STOPWATCH) because it is based on the book's code.

The MIT License does not cover the book's material listed under Credit.
