from utils.utils import auth_with_cookies, wait_for_url_param
from pages.search_results_page import SearchResultsPage
import pytest


@pytest.mark.parametrize("filters", [
    {"size": "M"}
], indirect=True)
def test_select_size_m(browser, filters):
    auth_with_cookies(browser)
    browser.get("https://www.hepsiburada.com/ara?q=k%C4%B1rm%C4%B1z%C4%B1%20elbise&ic=t&ico=t")
    search_page = SearchResultsPage(browser)
    search_page.select_size(filters["size"])
    wait_for_url_param(browser, f'filtreler=bedenler:{filters["size"]}')

    assert f'filtreler=bedenler:{filters["size"]}' in browser.current_url, \
        f"Size filter {filters['size']} not applied (no parameter in URL)"

