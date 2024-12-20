import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.MainNavigation import MainNavigation


class Login:

    def __init__(self, driver):
        self.driver = driver
        self.login_page_title = (By.XPATH, "//h1[.='Log in']")
        self.email_field = (By.ID, "email")
        self.password_field = (By.ID, "loginPassword")
        self.login_button = (By.XPATH, "//form[@class='login-form']//button[.='Log in']")
        self.field_error_message = (By.XPATH, "//ul[@class='invalid-feedback']/li")
        self.credentials_error_message = (By.XPATH, "//div[@role='alert']")
        self.login_subtitle = (By.XPATH, "//div[@class='heading-top']//div")
        self.forgot_password_link = (By.XPATH, "//a[.='Forgot your password?']")
        self.create_account_link = (By.XPATH, "//a[contains(., 'Create one')]")
        self.login_title_text = "Log in"
        self.login_subtitle_text = "Log in to your Madinah Moments account"

    def is_login_page_title_visible(self):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located(self.login_page_title))
        return page_title.is_displayed()

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def set_email_field(self, email, current_browser):
        self.driver.find_element(*self.email_field).click()
        self.driver.find_element(*self.email_field).clear()
        if current_browser == "safari":
            time.sleep(0.5)
        if email != "":
            self.driver.find_element(*self.email_field).send_keys(email)
        self.driver.find_element(*self.password_field).click()

    def set_password_field(self, password, current_browser):
        self.driver.find_element(*self.password_field).click()
        self.driver.find_element(*self.password_field).clear()
        if current_browser == "safari":
            time.sleep(0.5)
        if password != "":
            self.driver.find_element(*self.password_field).send_keys(password)
        self.driver.find_element(*self.email_field).click()

    def is_filed_error_message_visible(self):
        wait = WebDriverWait(self.driver, 30)
        message = wait.until(EC.visibility_of_element_located(self.field_error_message))
        return message.is_displayed()

    def get_field_error_message_text(self):
        return self.driver.find_element(*self.field_error_message).text

    def is_credentials_error_message_visible(self):
        wait = WebDriverWait(self.driver, 30)
        message = wait.until(EC.visibility_of_element_located(self.credentials_error_message))
        return message.is_displayed()

    def get_credentials_error_message_text(self):
        return self.driver.find_element(*self.credentials_error_message).text

    def full_log_in(self, email, password, browser):
        main_nav_obj = MainNavigation(self.driver)
        button = self.driver.find_elements(*main_nav_obj.login_button)
        if len(button) != 0:
            main_nav_obj.click_login_button()
            self.set_email_field(email, browser)
            self.set_password_field(password, browser)
            self.click_login_button()
            main_nav_obj.wait_page_to_load()

    def is_login_subtitle_visible(self):
        return self.driver.find_element(*self.login_subtitle).is_displayed()

    def get_login_subtitle_text(self):
        return self.driver.find_element(*self.login_subtitle).text

    def is_email_field_visible(self):
        return self.driver.find_element(*self.email_field).is_displayed()

    def is_password_field_visible(self):
        return self.driver.find_element(*self.password_field).is_displayed()

    def is_login_button_visible(self):
        return self.driver.find_element(*self.login_button).is_displayed()

    def is_login_button_enabled(self):
        button_class = self.driver.find_element(*self.login_button).get_attribute("class")
        return False if "disabled" in button_class else True

    def is_forgot_password_link_visible(self):
        return self.driver.find_element(*self.forgot_password_link).is_displayed()

    def is_create_account_link_visible(self):
        return self.driver.find_element(*self.create_account_link).is_displayed()

    def click_forgot_password_link(self):
        self.driver.find_element(*self.forgot_password_link).click()

    def click_create_account_link(self):
        self.driver.find_element(*self.create_account_link).click()
