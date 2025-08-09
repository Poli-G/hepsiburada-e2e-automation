from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By

class BasePage:
    def __init__(self, browser):
        self.browser = browser

    def wait_for_clickable(self, locator, timeout=10):
        wait = WebDriverWait(self.browser, timeout, ignored_exceptions=[StaleElementReferenceException])
        return wait.until(EC.element_to_be_clickable(locator))

    def wait_for_visible(self, locator, timeout=10):
        wait = WebDriverWait(self.browser, timeout)
        return wait.until(EC.visibility_of_element_located(locator))

    def click_with_js(self, element):
        self.browser.execute_script("arguments[0].click();", element)

    def scroll_to(self, element):
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)
