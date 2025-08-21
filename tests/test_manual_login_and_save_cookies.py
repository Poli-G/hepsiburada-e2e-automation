from utils.cookie_handler import save_cookies
import time


def test_manual_login_and_save_cookies(browser, base_url, logger):
    browser.get(base_url)
    logger.info("Login manually within 60 seconds...")
    time.sleep(60) # time for a manual login
    save_cookies(browser, "cookies.json")
    logger.info("Login manually within 60 seconds...")
