import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.LoginPage import Login
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass
from Common.config import EMAIL, PASSWORD


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestLogin(BaseClass):

    @severity(severity_level.BLOCKER)
    @allure.feature('Login')
    @allure.title("User is navigated to the Login page")
    @allure.issue("QP-382", "Story QP-382")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58781", "C58781")
    @pytest.mark.dependency(name="test_1")
    def test_1(self, driver):
        login_obj = Login(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(self.url)
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58781: Check the page title"):
            main_nav_obj.click_login_button()
            assert login_obj.is_login_page_title_visible()

    @severity(severity_level.BLOCKER)
    @allure.feature('Login')
    @allure.title("Login page appearance")
    @allure.issue("QP-382", "Story QP-382")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58782", "C58782")
    @pytest.mark.dependency(depends=["test_1"])
    def test_2(self, driver):
        login_obj = Login(driver)
        with check, allure.step("C58782: Page title is visible"):
            assert login_obj.is_login_page_title_visible()
        with check, allure.step("C58782: Page subtitle is visible"):
            assert login_obj.is_login_subtitle_visible()
        with check, allure.step("C58782: Email field is visible"):
            assert login_obj.is_email_field_visible()
        with check, allure.step("C58782: Password field is visible"):
            assert login_obj.is_password_field_visible()
        with check, allure.step("C58782: Login button is visible"):
            assert login_obj.is_login_button_visible()
        with check, allure.step("C58782: Forgot password link is visible"):
            assert login_obj.is_forgot_password_link_visible()
        with check, allure.step("C58782: Create account link is visible"):
            assert login_obj.is_create_account_link_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Login')
    @allure.title("Unsuccessfully login with email: {email} and password: {password}")
    @allure.issue("QP-382", "Story QP-382")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58783", "C58783")
    @allure.testcase("58784", "C58784")
    @allure.testcase("58785", "C58785")
    @allure.testcase("58785", "C58786")
    @pytest.mark.dependency(depends=["test_1"])
    @pytest.mark.parametrize('email,password,error,test_case', [
        (EMAIL[:-1], PASSWORD, "There was a problem logging you in. Please try again.", "C58784"),
        (EMAIL, PASSWORD[:-1], "There was a problem logging you in. Please try again.", "C58785"),
        (EMAIL.replace("@", ""), PASSWORD, "Please enter a valid email", "C58783"),
        ("", PASSWORD, "Please enter your email", "C58784"),
        (EMAIL, "", "Please enter your password", "C58785")
    ])
    def test_3(self, driver, email, password, error, test_case):
        current_browser = self.current_browser
        login_obj = Login(driver)
        driver.refresh()
        login_obj.set_email_field(email, current_browser)
        login_obj.set_password_field(password, current_browser)
        with check, allure.step(f"{test_case}: Check for error"):
            if "Please enter" in error:
                assert login_obj.is_filed_error_message_visible()
            else:
                login_obj.click_login_button()
                assert login_obj.is_credentials_error_message_visible()
        if "Please enter" in error:
            with check, allure.step("C58786: Login button is disabled"):
                assert not login_obj.is_login_button_enabled()
        with check, allure.step(f"{test_case}: Check the error text"):
            if "Please enter" in error:
                assert login_obj.get_field_error_message_text() == error
            else:
                assert login_obj.get_credentials_error_message_text() == error

    @severity(severity_level.CRITICAL)
    @allure.feature('Login')
    @allure.title("Successful login")
    @allure.issue("QP-382", "Story QP-382")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58787", "C58787")
    @pytest.mark.dependency(depends=["test_1"])
    def test_4(self, driver):
        current_browser = self.current_browser
        login_obj = Login(driver)
        main_nav_obj = MainNavigation(driver)
        driver.refresh()
        main_nav_obj.wait_page_to_load()
        login_obj.set_email_field(EMAIL, current_browser)
        login_obj.set_password_field(PASSWORD, current_browser)
        login_obj.click_login_button()
        main_nav_obj.wait_page_to_load()
        with check, allure.step("Logout button is visible"):
            assert main_nav_obj.is_logout_button_visible(current_browser)

    @severity(severity_level.CRITICAL)
    @allure.feature('Login')
    @allure.title("Successful logout")
    @allure.issue("QP-382", "Story QP-382")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58787", "C58787")
    @pytest.mark.dependency(depends=["test_1"])
    def test_5(self, driver):
        login_obj = Login(driver)
        main_nav_obj = MainNavigation(driver)
        driver.refresh()
        main_nav_obj.wait_page_to_load()
        main_nav_obj.click_logout_button()
        main_nav_obj.wait_page_to_load()
        with check, allure.step("Check for logout message"):
            assert login_obj.is_credentials_error_message_visible()
        with check, allure.step("Check the logout message text"):
            assert login_obj.get_credentials_error_message_text() == "You have been logged out."
