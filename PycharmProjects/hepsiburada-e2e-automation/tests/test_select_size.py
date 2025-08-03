from utils.utils import auth_with_cookies, wait_for_url_param
from pages.search_results_page import SearchResultsPage


def test_select_size_m(browser):
    auth_with_cookies(browser)
    browser.get("https://www.hepsiburada.com/ara?q=k%C4%B1rm%C4%B1z%C4%B1%20elbise&ic=t&ico=t")
    search_page = SearchResultsPage(browser)
    search_page.select_size_m()
    wait_for_url_param(browser, 'filtreler=bedenler:M')

    assert 'filtreler=bedenler:M' in browser.current_url, "Size filter M not applied (no parameter in URL)"
