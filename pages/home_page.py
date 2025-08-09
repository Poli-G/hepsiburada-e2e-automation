from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from locators.locators import HomePageLocators


class HomePage(BasePage):

    def open(self):
        self.browser.get("https://www.hepsiburada.com")

    def search(self, query):
        self.wait_for_clickable(HomePageLocators.SEARCH_BOX)
        search_box = self.wait_for_visible(HomePageLocators.SEARCH_BOX)
        self.scroll_to(search_box)
        self.browser.execute_script("arguments[0].click();", search_box)
        search_box = self.wait_for_visible(HomePageLocators.SEARCH_BOX)
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)

