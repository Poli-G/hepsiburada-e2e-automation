from utils.utils import auth_with_cookies, wait_for_url_param
from pages.search_results_page import SearchResultsPage
import pytest


@pytest.mark.parametrize("filters", [
    {"fabric": "Pamuk"}
], indirect=True)
def test_select_fabric(browser, filters):
    auth_with_cookies(browser)
    browser.get("https://www.hepsiburada.com/ara?q=k%C4%B1rm%C4%B1z%C4%B1%20elbise&ic=t&ico=t")
    search_page = SearchResultsPage(browser)
    search_page.select_fabric(filters["fabric"])
    wait_for_url_param(browser, f'Tipi:{filters["fabric"]}')

    assert f'Tipi:{filters["fabric"]}' in browser.current_url, "Fabric type Pamuk not applied (no parameter in URL)"
