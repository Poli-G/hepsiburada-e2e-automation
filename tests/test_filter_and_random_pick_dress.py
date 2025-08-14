import time
import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.utils import auth_with_cookies, wait_for_url_param


@pytest.mark.parametrize("filters", [
    {"size": "M", "fabric": "Pamuk", "price": {"min": 800, "max": 1200}}
], indirect=True)
def test_search_and_select_random_dress(browser, search_query, filters):
    auth_with_cookies(browser)
    home_page = HomePage(browser)

    home_page.search(search_query)
    search_results = SearchResultsPage(browser)
    search_results.close_overlay_if_present()

    initial_count = search_results.get_products_count_from_label()
    assert initial_count > 0, "No products found according to the label count"

    search_results.close_overlay_if_present()

    # Применяем фильтры
    if filters.get("size"):
        search_results.select_size(filters["size"])
        wait_for_url_param(browser, f'filtreler=bedenler:{filters["size"]}')
    if filters.get("fabric"):
        search_results.select_fabric(filters["fabric"])
    if filters.get("price"):
        price = filters["price"]
        search_results.select_price(price)

    # Обновляем страницу один раз, чтобы DOM и лейбл обновились
    browser.refresh()

    # Получаем новый count из лейбла
    new_count = search_results.get_products_count_from_label()
    assert new_count <= initial_count, f"Label count did not decrease after filters. Before: {initial_count}, After: {new_count}"

    # Теперь выбираем случайное платье
    selected_dress_name = search_results.select_random_dress()
    time.sleep(15)
    assert selected_dress_name, "Failed to select a random dress after filters"
