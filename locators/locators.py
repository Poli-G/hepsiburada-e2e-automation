from selenium.webdriver.common.by import By


class HomePageLocators:
    # SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder='Ürün, kategori veya marka ara']")
    SEARCH_BOX = (By.XPATH, '//*[@data-test-id="search-bar-input"]')


class SearchResultsLocators:
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class, 'productCard-module_productCardRoot')]")


class FilterPanelLocators:
    @staticmethod
    def fabric_checkbox(fabric_name):
        return (
            By.XPATH,
            f"//div[contains(@class, 'filter-panel')]//label[contains(., '{fabric_name}')]"
        )

    FILTER_PANEL = (By.ID, "stickyVerticalFilter")

    SIZE_FILTER_SCROLL_TARGET = (By.XPATH, "//label[@for='collapse-bedenler']//div[@data-test-id='collapse-title']")
    SIZE_COLLAPSE_ICON = (By.XPATH, "//label[.//div[text()='Beden']]//div[@data-test-id='collapse-icon']")
    M_SIZE_LABEL = (By.XPATH, '//input[@value="M"]/parent::label')
    M_SIZE_CHECKBOX = (By.XPATH,"//label[.//div[normalize-space(.)='Beden']]/following-sibling::div//input[@type='checkbox' and @value='M']")

    PRICE_FILTER_SCROLL_TARGET = (By.XPATH, "//label[@for ='collapse-fiyat'] // div[@ data-test-id='collapse-title']")
    PRICE_COLLAPSE_ICON = (By.XPATH, "//label[.//div[text()='Fiyat Aralığı']]//div[@data-test-id='collapse-icon']")
    PRICE_FROM_INPUT = (By.XPATH, "//input[@placeholder='En az' and @aria-label='En az']")
    PRICE_TO_INPUT = (By.XPATH, "//input[@placeholder='En çok' and @aria-label='En çok']")
    PRICE_APPLY_BUTTON =(By.XPATH, "//button[@aria-label='Filtrele']")



    FABRIC_FILTER_SCROLL_TARGET = (By.XPATH, "//label[starts-with(@for,'collapse-VariantList')]//div[@data-test-id='collapse-title' and text()='Kumaş Tipi']")
    FABRIC_COLLAPSE_ICON = (By.XPATH, "//label[.//div[text()='Kumaş Tipi']]//div[@data-test-id='collapse-icon']")
    PAMUK_LABEL = (By.XPATH, '//input[@value="Pamuk"]/parent::label')
    PAMUK_CHECKBOX = (By.XPATH,"//label[.//div[normalize-space()='Kumaş Tipi']]//following::input[@type='checkbox'and @value='Pamuk']")



