import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.LoginPage import Login
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=0.5, rerun_except="assert")
class TestLogin(BaseClass):
    current_browser = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestLogin.current_browser = request.node.callspec.params["driver"]

    @severity(severity_level.CRITICAL)
    @allure.feature('Login')
    @allure.title("User is navigated to the Login page")
    def test_1(self, driver):
        login_obj = Login(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(BaseClass.url)
        main_nav_obj.wait_page_to_load()
        with check, allure.step("Check the page title"):
            main_nav_obj.click_login_button()
            assert login_obj.is_login_page_title_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Login')
    @allure.title("Unsuccessfully login with email: {email} and password: {password}")
    @pytest.mark.parametrize('email,password,error', [
        (BaseClass.email[:-1], BaseClass.password, "There was a problem logging you in. Please try again."),
        (BaseClass.email, BaseClass.password[:-1], "There was a problem logging you in. Please try again."),
        (BaseClass.email.replace("@", ""), BaseClass.password, "Please enter a valid email"),
        ("", BaseClass.password, "Please enter your email"),
        (BaseClass.email, "", "Please enter your password")
    ])
    def test_2(self, driver, email, password, error):
        current_browser = TestLogin.current_browser
        login_obj = Login(driver)
        driver.refresh()
        login_obj.set_email_field(email, current_browser)
        login_obj.set_password_field(password, current_browser)
        with check, allure.step("Check for error"):
            if "Please enter" in error:
                assert login_obj.is_filed_error_message_visible()
            else:
                login_obj.click_login_button()
                assert login_obj.is_credentials_error_message_visible()
        with check, allure.step("Check the error text"):
            if "Please enter" in error:
                assert login_obj.get_field_error_message_text() == error
            else:
                assert login_obj.get_credentials_error_message_text() == error

    @severity(severity_level.CRITICAL)
    @allure.feature('Login')
    @allure.title("Successful login")
    def test_3(self, driver):
        current_browser = TestLogin.current_browser
        login_obj = Login(driver)
        main_nav_obj = MainNavigation(driver)
        driver.refresh()
        main_nav_obj.wait_page_to_load()
        login_obj.set_email_field(BaseClass.email, current_browser)
        login_obj.set_password_field(BaseClass.password, current_browser)
        login_obj.click_login_button()
        main_nav_obj.wait_page_to_load()
        with check, allure.step("Logout button is visible"):
            assert main_nav_obj.is_logout_button_visible(TestLogin.current_browser)

    @severity(severity_level.CRITICAL)
    @allure.feature('Login')
    @allure.title("Successful logout")
    def test_4(self, driver):
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
