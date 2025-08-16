from utils.cookie_handler import save_cookies
import time


def test_manual_login_and_save_cookies(browser, base_url):
    browser.get(base_url)
    print("Залогинься вручную в течение 60 секунд...")
    time.sleep(60)  # время вручную залогиниться
    save_cookies(browser, "cookies.json")
    print("Cookies сохранены")
