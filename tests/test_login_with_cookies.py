from utils.utils import auth_with_cookies


def test_login_with_cookies(browser):

    auth_with_cookies(browser)
    assert "Hesabım" in browser.page_source or "sipariş" in browser.page_source.lower()