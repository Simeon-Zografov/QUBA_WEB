import allure
import pytest
from allure import severity, severity_level
from axe_selenium_python import Axe
from Common.BaseClass import BaseClass
from Pages.MainNavigation import MainNavigation


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.only_chrome
class TestAccessibility(BaseClass):

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the home page accessibility")
    def test_1(self, driver):
        main_nav_obj = MainNavigation(driver)
        driver.get(BaseClass.url)
        main_nav_obj.wait_page_to_load()
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(results["violations"]) == 0

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the site page accessibility")
    def test_2(self, driver):
        main_nav_obj = MainNavigation(driver)
        main_nav_obj.click_sites_button()
        main_nav_obj.wait_page_to_load()
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(results["violations"]) == 0

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the about page accessibility")
    def test_3(self, driver):
        main_nav_obj = MainNavigation(driver)
        main_nav_obj.click_about_button()
        main_nav_obj.wait_page_to_load()
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(results["violations"]) == 0

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the events page accessibility")
    def test_4(self, driver):
        main_nav_obj = MainNavigation(driver)
        main_nav_obj.click_events_button()
        main_nav_obj.wait_page_to_load()
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(results["violations"]) == 0

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the sponsors page accessibility")
    def test_5(self, driver):
        main_nav_obj = MainNavigation(driver)
        main_nav_obj.click_sponsors_button()
        main_nav_obj.wait_page_to_load()
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(results["violations"]) == 0

    @severity(severity_level.NORMAL)
    @allure.feature('Accessibility')
    @allure.title("Check the contact page accessibility")
    def test_6(self, driver):
        main_nav_obj = MainNavigation(driver)
        main_nav_obj.click_contact_button()
        main_nav_obj.wait_page_to_load()
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        if len(results["violations"]) != 0:
            axe_report = axe.report(results["violations"])
            allure.attach(
                axe_report,
                name="Axe Accessibility Report",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert len(results["violations"]) == 0
