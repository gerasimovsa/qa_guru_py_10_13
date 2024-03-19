import os
import pytest
import allure
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils import attach
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser():
    with allure.step("Getting login and password from .env"):
        login = os.getenv("LOGIN")
        password = os.getenv("PASSWORD")
    with allure.step("Settings base url"):
        browser.config.base_url = "https://demoqa.com"
    with allure.step("Setting up timeout for browser"):
        browser.config.timeout = 10.0
    with allure.step("Setting up browser window size"):
        browser.config.window_width = 1920
        browser.config.window_height = 1200
    with allure.step("Setting up Selenoid remote executor"):
        options = Options()
        selenoid_capabilities = {
            "browserName": "chrome",
            "browserVersion": "120.0",
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True
            }
        }
        options.capabilities.update(selenoid_capabilities)
        driver = webdriver.Remote(
            command_executor=f"https://{login}:{password}@selenoid.autotests.cloud/wd/hub",
            options=options)
        browser.config.driver = driver

    yield

    attach.add_html(browser)
    attach.add_logs(browser)
    attach.add_screenshot(browser)
    attach.add_video(browser)

    browser.quit()
