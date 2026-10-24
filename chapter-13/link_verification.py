"""Check the links on a web page and report the ones that are broken.

Usage: python3 link_verification.py <url>

Opens the page in a headless Chrome browser using Playwright, then visits every
link on the page that points to another web page. Prints a message for each
link that returns a 404 "not found" error or can't be reached at all. Each
link is only checked once. Working links aren't printed, but a count of the
links checked is shown at the end.

Requires Playwright and requests (pip3 install playwright requests), plus the
browser Playwright uses (playwright install chromium).
"""

import sys, requests
from playwright.sync_api import sync_playwright, Error as PlaywrightError
from urllib.parse import urljoin, urldefrag


def main():

    # Check if the correct number of command line arguments is provided.
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 link_verification.py <url>")

    # Make sure the URL starts with http:// or https://.
    page_url = sys.argv[1]
    if not page_url.startswith(("http://", "https://")):
        sys.exit("The URL must start with http:// or https://")

    # Use Playwright to launch a browser and navigate to the provided URL.
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(page_url)
        except PlaywrightError:
            sys.exit(f"Could not open {page_url}")

        # Keep track of the links already checked, and count the broken ones.
        # The page's own address is included so links back to it are skipped.
        checked_urls = {urldefrag(page.url)[0]}
        broken_links = 0

        # Loop through all the anchor elements and check their href attributes.
        for elem in page.locator("a").all():

            # Skip any anchor elements without an href.
            href = elem.get_attribute("href")
            if not href:
                continue

            # Create an absolute URL from the page's address and the href, leaving off any #fragment.
            # page.url is used instead of page_url because the page may have been redirected.
            url = urldefrag(urljoin(page.url, href))[0]

            # Skip links that aren't web pages (mailto:, tel:, javascript:, etc.) and links already checked.
            if not url.startswith(("http://", "https://")) or url in checked_urls:
                continue
            checked_urls.add(url)

            # Check if the URL returns a 404 status code or is unreachable, and print a message if so.
            # stream=True skips downloading the page's contents, since only the status code is needed.
            try:
                with requests.get(url, timeout=10, stream=True) as res:
                    if res.status_code == 404:
                        print(f"Page could not be found: {url}")
                        broken_links += 1
            except requests.RequestException:
                print(f"Could not reach: {url}")
                broken_links += 1

        # Close the browser after checking all links.
        browser.close()

    print(f"Checked {len(checked_urls) - 1} links. {broken_links} broken.")


if __name__ == "__main__":
    main()
