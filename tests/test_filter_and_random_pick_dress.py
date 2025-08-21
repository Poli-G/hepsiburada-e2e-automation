import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.utils import auth_with_cookies


@pytest.mark.parametrize("filters", [
    {"size": "M", "fabric": "Pamuk", "price": {"min": 800, "max": 1200}}
], indirect=True)
def test_search_and_select_random_dress(browser, base_url, search_query, filters, logger):
    auth_with_cookies(browser, base_url)
    home_page = HomePage(browser, logger)
    home_page.search(search_query)
    search_results = SearchResultsPage(browser, logger)
    initial_count = search_results.get_products_count_from_label()
    assert initial_count > 0, "No products found according to the label count"
    search_results.apply_filters(filters)
    browser.refresh()
    new_count = search_results.get_products_count_from_label()
    assert new_count <= initial_count, f"Label count did not decrease after filters. Before: {initial_count}, After: {new_count}"

    selected_dress_name = search_results.select_random_dress()
    assert selected_dress_name, "Failed to select a random dress after filters"
