import pytest
from pages.home_page import HomePage
from pages.search_results_page import SearchResultsPage
from utils.utils import auth_with_cookies


@pytest.fixture
def search_query():
    return "kırmızı elbise"


def test_search_dress(browser, base_url, search_query):
    auth_with_cookies(browser, base_url)
    home_page = HomePage(browser)
    home_page.search(search_query)
    search_results = SearchResultsPage(browser)
    search_results.close_overlay_if_present()
    count = search_results.get_products_count()

    assert count > 0, "Product cards not found on page"

