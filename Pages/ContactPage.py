from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import random
import string


class ContactPage:

    def __init__(self, driver):
        self.driver = driver
        self.contact_button = (By.XPATH, "//a[.='Contact']")
        self.contact_page_title = (By.XPATH, "//h1[.='Get in touch']")
        self.success_message = (By.XPATH, "//div[@class='app-alert alert alert-success']")
        self.name_input_field = (By.ID, "name")
        self.email_input_field = (By.ID, "email")
        self.message_input_filed = (By.ID, "message")
        self.send_message_button = (By.XPATH, "//button[.='Send message']")

    def click_contact_button(self):
        self.driver.find_element(*self.contact_button).click()

    def is_contact_page_title_visible(self):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located(self.contact_page_title))
        return page_title.is_displayed()

    def is_success_message_visible(self):
        wait = WebDriverWait(self.driver, 30)
        message = wait.until(EC.visibility_of_element_located(self.success_message))
        return message.is_displayed()

    def set_name_field(self, name):
        self.driver.find_element(*self.name_input_field).send_keys(name)

    def set_email_field(self, email):
        self.driver.find_element(*self.email_input_field).send_keys(email)

    def set_message_field(self, message):
        self.driver.find_element(*self.message_input_filed).send_keys(message)

    def click_send_message_button(self):
        self.driver.find_element(*self.send_message_button).click()

    @classmethod
    def generate_random_name(cls):
        fake = Faker()
        return fake.name()

    @classmethod
    def generate_random_email(cls):
        fake = Faker()
        return fake.email()

    @classmethod
    def generate_random_message(cls):
        message_length = random.randint(1, 50)  # Random length up to 50
        return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=message_length)).strip()





