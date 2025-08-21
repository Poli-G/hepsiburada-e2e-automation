import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.wait import WebDriverWait
from utils.cookie_handler import load_cookies
from urllib.parse import urljoin
import logging
from colorama import Fore, Style


def auth_with_cookies(browser, base_url, cookie_file="cookies.json"):
    browser.get(base_url)
    load_cookies(browser, cookie_file)
    browser.refresh()


def open_path(browser, base_url, path):
    full_url = urljoin(base_url, path)
    browser.get(full_url)


def retry_find_element(find_element_func, logger, retries=3, delay=1):
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[{attempt}/{retries}] Attempt to find element...")
            element = find_element_func()
            logger.info("✅ Element found.")
            return element
        except StaleElementReferenceException as e:
            logger.warning(f"⚠️ Exception: {e}. Retry after {delay}s.")
            time.sleep(delay)
    raise Exception("Unable to find element after multiple attempts.")


def retry_click(find_element_func, logger, retries=3, delay=1):
    """
    Attempts to click on the element returned by `find_element_func`,
    retries if StaleElementReferenceException occurs.
    """
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[{attempt}/{retries}] Attempt to click on an element...")
            element = find_element_func()
            element.click()
            logger.info("Click successful.")
            return
        except StaleElementReferenceException as e:
            logger.warning(f"⚠Exception: {e}. Retry after {delay}s.")
            time.sleep(delay)
    raise Exception("Unable to click on element after multiple attempts.")


def retry_send_keys(find_element_func, text, logger=None, retries=3, delay=1):
    """
    Attempts to send keys to the element returned by `find_element_func`,
    retries if StaleElementReferenceException occurs.
    """
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[{attempt}/{retries}] Attempt to send keys '{text}' to an element...")
            element = find_element_func()
            element.clear()
            element.send_keys(text)
            logger.info("Input successful.")
            return
        except StaleElementReferenceException as e:
            logger.warning(f"Exception: {e}. Retry after {delay}s.")
            time.sleep(delay)
    raise Exception(f"Unable to send keys '{text}' to element after multiple attempts.")


def wait_for_url_param(driver, param: str, timeout: int = 10):
    """
    Waits for parameter to appear in URL.

        :param driver: WebDriver instance
        :param param: string to find in current_url
        :param timeout: timeout (default 10 seconds)
    """
    WebDriverWait(driver, timeout).until(
        lambda d: param in d.current_url
    )

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: Fore.LIGHTBLUE_EX,
        logging.INFO: Fore.LIGHTGREEN_EX,
        logging.WARNING: Fore.LIGHTYELLOW_EX,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }

    def format(self, record):
        if record.levelno in self.COLORS:
            record.levelname = (f"{self.COLORS[record.levelno]}"
                                f"{record.levelname}{Style.RESET_ALL}")
            record.msg = (f"{self.COLORS[record.levelno]}"
                          f"{record.msg}{Style.RESET_ALL}")

        return super().format(record)

