from utils.utils import auth_with_cookies, wait_for_url_param
from pages.search_results_page import SearchResultsPage
import pytest

@pytest.fixture
def price_range():
    return {"min": "800", "max": "1200"}


def test_select_size_m(browser, price_range):
    auth_with_cookies(browser)
    browser.get("https://www.hepsiburada.com/ara?q=k%C4%B1rm%C4%B1z%C4%B1%20elbise&ic=t&ico=t")
    search_page = SearchResultsPage(browser)
    search_page.select_price(price_range)
    wait_for_url_param(browser, f"fiyat:{price_range['min']}-{price_range['max']}")

    assert f"fiyat:{price_range['min']}-{price_range['max']}" in browser.current_url, "Price not applied (no parameter in URL)"
