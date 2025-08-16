from utils.utils import auth_with_cookies


def test_login_with_cookies(browser, base_url):

    auth_with_cookies(browser, base_url)
    assert "Hesabım" in browser.page_source or "sipariş" in browser.page_source.lower()
