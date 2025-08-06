from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.locators import SearchResultsLocators, FilterPanelLocators
import time
from utils.utils import retry_click, retry_send_keys


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

    def select_size_m(self):
        print("⏳ Ждем загрузки панели фильтров...")
        filter_panel = WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )
        print("✅ Панель фильтров найдена")

        # 1. Скроллим до заголовка "Размер"
        size_filter_title = WebDriverWait(filter_panel, 10).until(
            lambda panel: panel.find_element(*FilterPanelLocators.SIZE_FILTER_SCROLL_TARGET)
        )
        self.browser.execute_script("""
            arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;
        """, filter_panel, size_filter_title)
        print("📜 Выполнили скролл до заголовка фильтра размера")

        time.sleep(0.3)

        # 2. Кликаем по стрелочке, чтобы развернуть список размеров
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(FilterPanelLocators.SIZE_COLLAPSE_ICON)
        ))
        print("👆 Открыли список размеров")

        time.sleep(0.3)

        # 3. Заново находим панель и чекбокс M
        filter_panel = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )
        size_checkbox = WebDriverWait(filter_panel, 10).until(
            lambda panel: panel.find_element(*FilterPanelLocators.M_SIZE_CHECKBOX)
        )

        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", size_checkbox)
        print("📜 Проскроллили до чекбокса размера M")

        time.sleep(0.3)

        # 4. Кликаем по чекбоксу с ретраем
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(FilterPanelLocators.M_SIZE_CHECKBOX)
        ))
        print("👆 Кликнули по чекбоксу размера M")

        # 5. Дожидаемся, пока он реально станет выбранным
        WebDriverWait(self.browser, 10).until(
            lambda d: 'filtreler=bedenler:M' in d.current_url
        )

    def select_price(self, price_range: dict):
        print("⏳ Ждем загрузки панели фильтров...")
        filter_panel = WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )
        print("✅ Панель фильтров найдена")

        # 1. Скроллим до заголовка "цена"
        price_filter_title = WebDriverWait(filter_panel, 10).until(
            lambda panel: panel.find_element(*FilterPanelLocators.PRICE_FILTER_SCROLL_TARGET)
        )
        self.browser.execute_script("""
            arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;
        """, filter_panel, price_filter_title)
        print("📜 Выполнили скролл до заголовка фильтра цены")

        time.sleep(0.3)

        # 2. Кликаем по стрелочке, чтобы развернуть цену
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(FilterPanelLocators.PRICE_COLLAPSE_ICON)
        ))
        print("👆 Открыли список цен")

        time.sleep(0.3)

        # 3. Заново находим панель и инпут цен
        filter_panel = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )
        price_from_input = WebDriverWait(filter_panel, 10).until(
            lambda panel: panel.find_element(*FilterPanelLocators.PRICE_FROM_INPUT)
        )

        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", price_from_input)
        print("📜 Проскроллили до инпута ОТ")

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

        # 5. Дожидаемся, пока цена реально станет выбранной
        WebDriverWait(self.browser, 10).until(
            lambda d: f"fiyat:{price_range["min"]}-{price_range["max"]}" in d.current_url
        )

    def select_fabric(self, fabric_name):
        print("⏳ Ждем загрузки панели фильтров...")
        filter_panel = WebDriverWait(self.browser, 15).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )
        print("✅ Панель фильтров найдена")

        # 1. Скроллим до заголовка "ТИП ТКАНИ"
        fabric_filter_title = WebDriverWait(filter_panel, 10).until(
            lambda panel: panel.find_element(*FilterPanelLocators.FABRIC_FILTER_SCROLL_TARGET)
        )
        self.browser.execute_script("""
            arguments[0].scrollTop = arguments[1].offsetTop - arguments[0].offsetTop;
        """, filter_panel, fabric_filter_title)
        print("📜 Выполнили скролл до заголовка фильтра ткани")

        time.sleep(0.3)

        # 2. Кликаем по стрелочке, чтобы развернуть список типов ткани
        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(FilterPanelLocators.FABRIC_COLLAPSE_ICON)
        ))
        print("👆 Открыли список типов ткани")

        time.sleep(0.3)

        # 3. Получаем нужный локатор чекбокса по имени ткани
        checkbox_locator = getattr(FilterPanelLocators, f"{fabric_name.upper()}_CHECKBOX", None)
        if not checkbox_locator:
            raise ValueError(f"❌ Локатор для типа ткани '{fabric_name}' не найден!")

        # 3. Заново находим панель и тип pamuk
        filter_panel = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(FilterPanelLocators.FILTER_PANEL)
        )
        fabric_checkbox = WebDriverWait(filter_panel, 10).until(
            lambda panel: panel.find_element(*checkbox_locator)
        )

        self.browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", fabric_checkbox)
        print(f"📜 Проскроллили до чекбокса {fabric_name.upper()}")

        time.sleep(0.3)

        retry_click(lambda: WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(checkbox_locator)
        ))
        print(f"👆 Кликнули по чекбоксу типа {fabric_name}")

        # 5. Проверяем URL
        WebDriverWait(self.browser, 10).until(
            lambda d: f'Tipi:{fabric_name}' in d.current_url
        )
