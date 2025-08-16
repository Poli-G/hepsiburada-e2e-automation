import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.cookie_handler import load_cookies
import sys
import os
from data.base_filters import BASE_FILTERS
import copy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.hepsiburada.com",
        help="Base URL for the test"
    )


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def browser():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 2,
        "profile.default_content_setting_values.geolocation": 2
    })
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def authenticated_browser(browser, base_url):
    browser.get(base_url)  # важно: зайти до загрузки cookies
    load_cookies(browser, "cookies.json")
    browser.refresh()  # обновить, чтобы cookies подгрузились
    return browser


@pytest.fixture
def search_query():
    return "kırmızı elbise"


@pytest.fixture
def filters(request):
    data = copy.deepcopy(BASE_FILTERS)
    if hasattr(request, "param") and request.param:
        for key, value in request.param.items():
            if isinstance(value, dict) and isinstance(data.get(key), dict):
                data[key].update(value)
            else:
                data[key] = value
    return data
