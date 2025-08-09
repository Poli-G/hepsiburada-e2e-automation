from utils.cookie_handler import save_cookies
import time


def test_manual_login_and_save_cookies(browser):
    browser.get("https://www.hepsiburada.com/")
    print("Залогинься вручную в течение 60 секунд...")
    time.sleep(60)  # время вручную залогиниться
    save_cookies(browser, "cookies.json")
    print("Cookies сохранены")
