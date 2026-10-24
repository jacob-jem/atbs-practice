"""Download photos from Unsplash that match one or more search keywords.

Usage: python3 unsplash_downloader.py -s <keyword> [<keyword> ...] [-n <number>]

Example: python3 unsplash_downloader.py -s ocean sunset -n 3

Opens the Unsplash search results for the keywords in Chrome using Selenium and
downloads the first <number> photos (5 by default) to a folder called
"Unsplash Photos" on the desktop. If more photos are needed than the page
shows, it scrolls down and clicks "Load more". Photos are saved as
"<keywords> #<number>.<type>", numbered from 1, and a file with the same name
is overwritten. The browser is always closed when the program ends.

Requires Selenium and requests (pip3 install selenium requests) and Google
Chrome. The photos are found using Unsplash's current page layout and CSS class
names, so this program may stop working if the site changes them. Unsplash may
also block or restrict automated access, so check its terms before using it.
"""

import requests, argparse, re
from pathlib import Path
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# The folder on the desktop where the photos are saved.
DOWNLOAD_FOLDER = Path.home() / "Desktop" / "Unsplash Photos"

# The CSS class of the "Load more" button. The part after the dash looks
# automatically generated, so it may change when Unsplash updates its site.
LOAD_MORE_SELECTOR = ".loadMoreButton-FHXj5M"

# How many times to scroll down and click "Load more" while looking for one
# photo before giving up.
MAX_LOAD_ATTEMPTS = 3


def main():

    # Set up the command line arguments for the search keywords and number of photos to download.
    argparser = argparse.ArgumentParser(
        description="Search Unsplash for photos matching one or more keywords, and download the top results."
    )
    argparser.add_argument(
        "-s", "--search",
        help="One or more search keywords (e.g. -s ocean sunset)",
        required=True,
        nargs="+"
    )
    argparser.add_argument(
        "-n", "--number",
        help="Number of photos to download",
        default=5,
        type=int
    )
    args = argparser.parse_args()

    # Make sure at least one photo is requested.
    if args.number < 1:
        argparser.error("--number must be at least 1")

    # Locate or create a folder on the desktop to save the downloaded photos.
    DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    # Join the search keywords into a single string. A version with "/" replaced is used in
    # filenames, since a "/" in a filename would be treated as a folder.
    keywords = " ".join(args.search)
    file_prefix = keywords.replace("/", "-")

    downloaded_photos = 0
    browser = webdriver.Chrome()

    try:
        # Open the Unsplash search results page for the keywords.
        browser.get(f"https://unsplash.com/s/photos/{quote(keywords, safe='')}")

        # Loop through the search results and download the specified number of photos.
        # Once "Load more" fails to click, it isn't tried again.
        load_more_available = True
        i = 0
        while downloaded_photos < args.number:
            i += 1
            photo_selector = f"figure[data-masonryposition=\"{i}\"] img"

            # Look for the photo. If it's not on the page yet, keep loading more results and
            # looking again, up to a few attempts.
            photo_elem = find_photo(browser, photo_selector)
            attempts = 0
            while photo_elem is None and attempts < MAX_LOAD_ATTEMPTS:
                attempts += 1

                # Scroll to the bottom of the page, then click "Load more" unless that already failed.
                browser.find_element(By.TAG_NAME, "html").send_keys(Keys.END)
                load_more_available = load_more_available and click_load_more(browser)

                # Look for the photo again, giving the page a few seconds to load it.
                photo_elem = find_photo(browser, photo_selector, wait=5)

                # If "Load more" can't be clicked and the photo still isn't there, there are no more photos.
                if photo_elem is None and not load_more_available:
                    break

            if photo_elem is None:
                print(f"No more photos found after search result {i - 1}.")
                break

            # Get the srcset attribute (a list of image URLs with their widths) and pick the
            # 900px-wide image, which is the one without a watermark.
            srcset = photo_elem.get_attribute("srcset") or ""
            match = re.search(r"(https://\S+) 900w,", srcset)
            if not match:
                print(f"Skipped search result {i}: no 900px-wide image found.")
                continue

            # Download the photo, and move on to the next one if it can't be downloaded.
            try:
                res = requests.get(match.group(1), timeout=10)
                res.raise_for_status()
            except requests.RequestException:
                print(f"Skipped search result {i}: could not download it.")
                continue

            # Get the file type (such as jpeg) from the response and save the photo to the folder.
            # The photos are numbered by how many have been downloaded, so there are no gaps.
            ext = res.headers.get("Content-Type", "image/jpeg").split("/")[-1]
            photo_file = DOWNLOAD_FOLDER / f"{file_prefix} #{downloaded_photos + 1}.{ext}"
            print(f"Downloading {photo_file.name}...")
            with open(photo_file, "wb") as image_file:
                for chunk in res.iter_content(100000):
                    image_file.write(chunk)

            # Increment the count of downloaded photos.
            downloaded_photos += 1

    except KeyboardInterrupt:
        print("Stopped.")

    except NoSuchWindowException:
        print("The browser window was closed before the downloads finished.")

    # Always close the browser, even if an error occurs.
    finally:
        browser.quit()

    print(f"Downloaded {downloaded_photos} photos.")


def find_photo(browser, selector, wait=0):
    """Return the photo element for a CSS selector, or None if it isn't found within `wait` seconds."""
    try:
        return WebDriverWait(browser, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
    except TimeoutException:
        return None


def click_load_more(browser):
    """Click the "Load more" button and return True, or return False if it can't be clicked within 10 seconds."""
    try:
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, LOAD_MORE_SELECTOR))
        ).click()
        return True
    except TimeoutException:
        return False


if __name__ == "__main__":
    main()
