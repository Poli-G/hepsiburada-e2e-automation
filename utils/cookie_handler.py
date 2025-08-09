import json
import os


def save_cookies(driver, path):
    with open(path, 'w') as file:
        json.dump(driver.get_cookies(), file)


def load_cookies(driver, path):
    if not os.path.exists(path):
        return
    with open(path, 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
