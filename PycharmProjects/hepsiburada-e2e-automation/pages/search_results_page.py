from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import SearchResultsLocators, FilterPanelLocators
import time
from utils.utils import retry_click, retry_send_keys, retry_find_element


class SearchResultsPage:
    def __init__(self, browser):
        self.browser = browser

    def get_products_count(self):
        products = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_any_elements_located(SearchResultsLocators.PRODUCT_CARD)
        )
        return len(products)

    def wait_for_products(self, locator, timeout=10):
        return WebDriverWait(self.browser, timeout).until(
            EC.visibility_of_any_elements_located(locator)
        )

    def wait_for_filter_panel(self):
        return WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )

    def scroll_to_element_in_panel(self, target_locator):
        panel = self.wait_for_filter_panel()
        target = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(target_locator)
        )
        self.browser.execute_script(
            "arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;",
            panel, target
        )
        time.sleep(0.25)
        return target

    def expand_filter(self, expand_icon_locator):
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(expand_icon_locator)
        ))
        time.sleep(0.3)

    def click_checkbox_in_filter(self, checkbox_locator):
        filter_panel = self.wait_for_filter_panel()
        checkbox = WebDriverWait(filter_panel, 10).until(lambda p: p.find_element(*checkbox_locator))
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
        time.sleep(0.3)
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(checkbox_locator)
        ))

    def select_size(self, size: str):
        # 1. Скроллим внутри панели до заголовка "Beden"
        self.scroll_to_element_in_panel((
            By.XPATH,
            "//label[@for='collapse-bedenler']//div[@data-test-id='collapse-title']"
        ))

        # 2. Разворачиваем блок
        self.expand_filter((
            By.XPATH,
            "//label[.//div[text()='Beden']]//div[@data-test-id='collapse-icon']"
        ))

        # 3. Кликаем по нужному размеру (label, а не input)
        size_label_locator = (By.XPATH, f'//input[@value="{size}"]/parent::label')
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(size_label_locator)
        ))

        # 4. Ждём, пока фильтр применится
        WebDriverWait(self.browser, 10).until(
            lambda d: f'filtreler=bedenler:{size}' in d.current_url
        )

    def select_price(self, price_range: dict):
        panel = self.wait_for_filter_panel()

        self.scroll_to_element_in_panel(FilterPanelLocators.PRICE_FILTER_SCROLL_TARGET)

        self.expand_filter(FilterPanelLocators.PRICE_COLLAPSE_ICON)
        filter_panel = self.wait_for_filter_panel()
        price_from_input = WebDriverWait(filter_panel, 10).until(
            lambda p: p.find_element(*FilterPanelLocators.PRICE_FROM_INPUT)
        )
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", price_from_input)
        time.sleep(0.3)

        retry_send_keys(
            lambda: WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(FilterPanelLocators.PRICE_FROM_INPUT)
            ),
            price_range["min"]
        )

        retry_send_keys(
            lambda: WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(FilterPanelLocators.PRICE_TO_INPUT)
            ),
            price_range["max"]
        )

        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(FilterPanelLocators.PRICE_APPLY_BUTTON)
        ))

        WebDriverWait(self.browser, 10).until(
            lambda d: f"fiyat:{price_range['min']}-{price_range['max']}" in d.current_url
        )

    def select_fabric(self, fabric_name):

        panel = self.wait_for_filter_panel()

        self.scroll_to_element_in_panel(FilterPanelLocators.FABRIC_FILTER_SCROLL_TARGET)

        self.expand_filter(FilterPanelLocators.FABRIC_COLLAPSE_ICON)

        checkbox_locator = getattr(FilterPanelLocators, f"{fabric_name.upper()}_CHECKBOX", None)
        if not checkbox_locator:
            raise ValueError(f"Locator for the '{fabric_name}' does not found")

        self.click_checkbox_in_filter(checkbox_locator)

        WebDriverWait(self.browser, 10).until(
            lambda d: f'Tipi:{fabric_name}' in d.current_url
        )
