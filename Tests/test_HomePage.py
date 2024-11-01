import time

import allure
import pytest
from pytest_check import check
from allure import severity, severity_level

from Common import APIRequests
from Pages.HomePage import HomePage
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
class TestHomePage(BaseClass):
    current_browser = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestHomePage.current_browser = request.node.callspec.params["driver"]

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("User is navigated to the Home page")
    def test_1(self, driver):
        home_page_obj = HomePage(driver)
        driver.get(BaseClass.url)
        with check, allure.step("Check the page title"):
            assert home_page_obj.is_home_page_title_visible()
        with check, allure.step("Logo is visible"):
            assert home_page_obj.is_app_logo_visible()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check main navigation")
    def test_2(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("User is navigated to Sites page"):
            home_page_obj.click_sites_button()
            assert home_page_obj.is_sites_page_title_visible()
        with check, allure.step("User is navigated to Home page"):
            home_page_obj.click_home_button()
            assert home_page_obj.is_home_page_title_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check language switch")
    def test_3(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("English is selected by default"):
            assert home_page_obj.get_page_language() == "en-US"
        with check, allure.step("Successful language change"):
            home_page_obj.click_language_switch_button()
            home_page_obj.click_language_button()
            if TestHomePage.current_browser == "safari":
                time.sleep(0.5)
            assert home_page_obj.get_page_language() == "ar-SA"
