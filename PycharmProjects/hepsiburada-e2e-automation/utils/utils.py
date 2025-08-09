import time
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from utils.cookie_handler import load_cookies


def auth_with_cookies(browser, cookie_file="cookies.json"):
    browser.get("https://www.hepsiburada.com/")
    load_cookies(browser, cookie_file)
    browser.refresh()


def retry_find_element(find_element_func, retries=3, delay=1):
    for attempt in range(1, retries + 1):
        try:
            print(f"[{attempt}/{retries}] Attempt to find element...")
            element = find_element_func()
            print("✅ Element found.")
            return element
        except StaleElementReferenceException:
            print(f"⚠️ StaleElementReferenceException on find. Retry after {delay}s.")
            time.sleep(delay)
    raise Exception("❌ Unable to find element after multiple attempts.")


def retry_click(find_element_func, retries=3, delay=1):
    """
    Attempts to click on the element returned by `find_element_func`,
    retries if StaleElementReferenceException occurs.
    """
    for attempt in range(1, retries + 1):
        try:
            print(f"[{attempt}/{retries}] Attempt to click on an element...")
            element = find_element_func()
            element.click()
            print("✅ Click successful.")
            return
        except StaleElementReferenceException:
            print(f"⚠️ StaleElementReferenceException. Повтор через {delay}с.")
            time.sleep(delay)
    raise Exception("❌ Unable to click on element after multiple attempts.")


def retry_send_keys(find_element_func, text, retries=3, delay=1):
    """
    Attempts to send keys to the element returned by `find_element_func`,
    retries if StaleElementReferenceException occurs.
    """
    for attempt in range(1, retries + 1):
        try:
            print(f"[{attempt}/{retries}] Attempt to send keys '{text}' to an element...")
            element = find_element_func()
            element.clear()
            element.send_keys(text)
            print("✅ Input successful.")
            return
        except StaleElementReferenceException:
            print(f"⚠️ StaleElementReferenceException. Повтор через {delay}с.")
            time.sleep(delay)
    raise Exception(f"❌ Unable to send keys '{text}' to element after multiple attempts.")


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
