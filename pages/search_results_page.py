import random
import re

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import SearchResultsLocators, FilterPanelLocators
import time
from utils.utils import retry_click, retry_send_keys, retry_find_element


class SearchResultsPage:
    def __init__(self, browser):
        self.browser = browser

    def close_overlay_if_present(self, timeout=5):
        try:
            overlay_element = WebDriverWait(self.browser, timeout).until(
                EC.presence_of_element_located(SearchResultsLocators.OVERLAY)
            )
            window_size = self.browser.get_window_size()
            x = window_size['width'] // 2
            y = window_size['height'] // 2

            actions = ActionChains(self.browser)
            actions.move_by_offset(x, y).click().perform()

            WebDriverWait(self.browser, timeout).until(
                EC.invisibility_of_element(overlay_element)
            )
        except TimeoutException:
            pass

    def get_products_count(self):
        products = retry_find_element(
            lambda: WebDriverWait(self.browser, 10).until(
                EC.visibility_of_any_elements_located(SearchResultsLocators.PRODUCT_CARD)
            )
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
        self.scroll_to_element_in_panel((FilterPanelLocators.SIZE_FILTER_SCROLL_TARGET))

        # 2. Разворачиваем блок
        # self.expand_filter((FilterPanelLocators.SIZE_COLLAPSE_ICON))

        # 3. Кликаем по нужному размеру
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

    def apply_filters(self, filters):
        self.close_overlay_if_present()
        for filter_name, filter_value in filters.items():
            if filter_name == "size":
                self.select_size(filter_value)
            elif filter_name == "fabric":
                self.select_fabric(filter_value)
            elif filter_name == "price":
                self.select_price(filter_value)
            self.close_overlay_if_present()

    def get_products_count_from_label(self):
        element = retry_find_element(
            lambda: WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located(SearchResultsLocators.PRODUCT_COUNT_LABEL)
            )
        )
        # Берём текст напрямую через JS, чтобы точно актуальное
        text = self.browser.execute_script("return arguments[0].textContent;", element)
        numbers = re.findall(r'\d+', text.replace('.', ''))
        return int(numbers[0]) if numbers else 0

    def wait_until_label_count_changes(self, initial_count, timeout=10):
        """Ждёт, пока количество товаров на лейбле изменится."""
        WebDriverWait(self.browser, timeout).until(
            lambda driver: self.get_products_count_from_label() != initial_count,
            f"Product count did not change from {initial_count} within {timeout} seconds"
        )

    def get_and_verify_initial_count(self):
        """Получаем количество товаров и проверяем, что оно больше нуля"""
        count = self.get_products_count_from_label()
        assert count > 0, "No products found according to the label count"
        return count

    def refresh_and_verify_count(self, previous_count: int):
        """Обновляем страницу и проверяем, что количество товаров уменьшилось или осталось тем же"""
        self.browser.refresh()
        new_count = self.get_products_count_from_label()
        assert new_count <= previous_count, f"Label count did not decrease after filters. Before: {previous_count}, After: {new_count}"
        return new_count

    def select_random_dress (self):
        # Берём актуальное количество товаров через твою функцию
        total_count = self.get_products_count_from_label()
        if total_count == 0:
            raise Exception("No products found on the page")

        # Выбираем случайный индекс от 0 до total_count-1
        random_index = random.randint(0, total_count - 1)

        # Локатор всех карточек товаров
        product_locator = SearchResultsLocators.PRODUCT_CARD

        def get_product_at_index(index):
            # Находим все карточки
            elements = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located(product_locator)
            )
            # Если нужной карточки ещё нет, скроллим вниз и ждём
            while len(elements) <= index:
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                elements = self.browser.find_elements(*product_locator)
            return elements[index]

        # Берём элемент по индексу с ретраем на случай StaleElement
        product = retry_find_element(lambda: get_product_at_index(random_index))

        # Скроллим до него, чтобы точно был в зоне видимости
        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", product)
        time.sleep(0.5)  # немного подождать анимацию

        # Получаем название платья (если нужно)
        name = product.text

        # Кликаем по нему
        product.click()

        return name