import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login:

    def __init__(self, driver):
        self.driver = driver
        self.login_page_title = (By.XPATH, "//h1[.='Log in']")
        self.email_field = (By.ID, "email")
        self.password_field = (By.ID, "loginPassword")
        self.login_button = (By.XPATH, "//form[@class='login-form']//button[.='Log in']")
        self.field_error_message = (By.XPATH, "//ul[@class='invalid-feedback']/li")
        self.credentials_error_message = (By.XPATH, "//div[@role='alert']")

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


