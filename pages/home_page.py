from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from pages.base_page import BasePage
from utils.utils import retry_click
from locators.locators import HomePageLocators


class HomePage(BasePage):

    def open(self, base_url):
        self.browser.get(base_url)

    def search(self, query):
        def find_and_click():
            element = self.browser.find_element(*HomePageLocators.SEARCH_INPUT)
            try:
                element.click()
            except ElementClickInterceptedException:
                self.browser.execute_script("arguments[0].click();", element)
            return element

        retry_click(find_and_click, logger=self.logger)

        search_box = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(HomePageLocators.SEARCH_BOX)
        )

        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

        # encoded_query = quote_plus(query)
        #
        # WebDriverWait(self.browser, 10).until(
        #     lambda d: encoded_query.lower() in d.current_url.lower()
        # )
