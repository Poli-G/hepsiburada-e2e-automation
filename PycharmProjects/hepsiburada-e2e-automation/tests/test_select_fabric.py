from utils.utils import auth_with_cookies, wait_for_url_param
from pages.search_results_page import SearchResultsPage


def test_select_fabric(browser):
    auth_with_cookies(browser)
    browser.get("https://www.hepsiburada.com/ara?q=k%C4%B1rm%C4%B1z%C4%B1%20elbise&ic=t&ico=t")
    search_page = SearchResultsPage(browser)
    search_page.select_fabric()
    wait_for_url_param(browser, 'Tipi:Pamuk')

    assert 'Tipi:Pamuk' in browser.current_url, "Fabric type Pamuk not applied (no parameter in URL)"
