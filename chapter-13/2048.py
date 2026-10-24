"""Play 2048 by pressing random arrow keys until the game ends.

Usage: python3 2048.py

Opens https://play2048.co/ in Chrome using Selenium, presses a random arrow
key every 0.2 seconds, and stops when the "Game Over" message appears. Press
Ctrl-C to stop early. The browser is always closed when the program ends.

Requires Selenium (pip3 install selenium) and Google Chrome. The "Game Over"
message is found using the website's current CSS class names, so this program
may stop working if the site changes them. If no "Game Over" message appears
after 2000 key presses, the program stops and says so.
"""

import random, sys, time
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

URL = "https://play2048.co/"

# The arrow keys to choose from.
DIRECTIONS = [Keys.UP, Keys.DOWN, Keys.LEFT, Keys.RIGHT]

# The CSS classes of the "Game Over" message.
# The backslash escapes the colon in the class name "md:text-5xl".
GAME_OVER_SELECTOR = "div.text-4xl.font-semibold.md\\:text-5xl"

# Seconds to wait between key presses.
PAUSE = 0.2

# A random game ends well before this many key presses, so reaching it
# means something is wrong (for example, the site changed its layout).
MAX_PRESSES = 2000


def main():

    # Set up the Chrome browser. "eager" stops waiting for the page to load
    # once its HTML is ready, so slow ad scripts can't make the page hang.
    options = Options()
    options.page_load_strategy = "eager"
    browser = webdriver.Chrome(options=options)

    try:
        browser.get(URL)

        # Get the HTML element to send key presses to.
        html_elem = browser.find_element(By.TAG_NAME, "html")

        # Press a random arrow key every fraction of a second until the game is over.
        presses = 0
        while not is_game_over(browser):
            if presses == MAX_PRESSES:
                sys.exit(
                    f'No "Game Over" message after {MAX_PRESSES} key presses. '
                    "The website may have changed."
                )
            html_elem.send_keys(random.choice(DIRECTIONS))
            presses += 1
            time.sleep(PAUSE)

        print("Game Over!")

    except KeyboardInterrupt:
        print("Stopped.")

    except NoSuchWindowException:
        print("The browser window was closed before the game ended.")

    # Always close the browser, even if an error occurs.
    finally:
        browser.quit()


def is_game_over(browser):
    """Return True if the "Game Over" message is showing on the page."""

    # The message may be in the page's HTML before it's visible, so check both.
    for elem in browser.find_elements(By.CSS_SELECTOR, GAME_OVER_SELECTOR):
        if "Game Over" in elem.text and elem.is_displayed():
            return True
    return False


if __name__ == "__main__":
    main()
