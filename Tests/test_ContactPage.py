import time

import allure
import pytest
from pytest_check import check
from allure import severity, severity_level

from Common import Email
from Pages.ContactPage import ContactPage
from Pages.HomePage import HomePage
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
class TestContactPage(BaseClass):
    current_browser = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestContactPage.current_browser = request.node.callspec.params["driver"]

    @severity(severity_level.CRITICAL)
    @allure.feature('Contact page')
    @allure.title("User is navigated to the Contact page")
    def test_1(self, driver):
        contact_obj = ContactPage(driver)
        home_page_obj = HomePage(driver)
        driver.get(BaseClass.url)
        home_page_obj.wait_page_to_load()
        contact_obj.click_contact_button()
        with check, allure.step("Check the page title"):
            assert contact_obj.is_contact_page_title_visible()

    @severity(severity_level.CRITICAL)
    @allure.feature('Contact page')
    @allure.title("Successful message send")
    def test_2(self, driver):
        contact_obj = ContactPage(driver)
        random_name = contact_obj.generate_random_name()
        random_email = TestContactPage.current_browser + "_" + contact_obj.generate_random_email()
        random_message = contact_obj.generate_random_message()
        contact_obj.set_name_field(random_name)
        contact_obj.set_email_field(random_email)
        contact_obj.set_message_field(random_message)
        contact_obj.click_send_message_button()
        time.sleep(10)
        with check, allure.step("Success message is visible"):
            assert contact_obj.is_success_message_visible()
        expected_email = f"Full name: {random_name}\r\nEmail address: {random_email}\r\nYour message: {random_message}\r\n"
        actual_email = Email.get_latest_email_content(TestContactPage.current_browser)
        with check, allure.step("Email is correct"):
            assert actual_email == expected_email
