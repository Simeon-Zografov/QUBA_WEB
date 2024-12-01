from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from faker import Faker
import random
import string

from Common.BaseClass import BaseClass


class ContactPage:

    def __init__(self, driver):
        self.driver = driver
        self.contact_page_title = (By.XPATH, "//h1")
        self.success_message = (By.XPATH, "//div[@class='app-alert alert alert-success']")
        self.name_input_field = (By.ID, "name")
        self.email_input_field = (By.ID, "email")
        self.message_input_field = (By.ID, "message")
        self.send_message_button = (By.XPATH, "//button[.='Send message']")
        self.heading_description = (By.XPATH, "//div[@class='heading-top']//div")
        self.message_section = (By.XPATH, "//div[@class='main-details']")
        self.details_section = (By.XPATH, "//aside[@class='secondary-details']")
        self.transport_section = (By.XPATH, "//section[@class='site-travel-info']")
        self.invalid_email_error = (By.XPATH, "//div[contains(@class, 'email-input')]//ul["
                                              "@class='invalid-feedback']//li")
        self.footer = (By.ID, "site-footer")
        self.name_field_placeholder = "Full name"
        self.email_field_placeholder = "Email address"
        self.invalid_email_error_message = "Please enter a valid email"
        self.message_field_placeholder = "Your message"

    def is_contact_page_title_visible(self, title):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[.='{title}']")))
        return page_title.is_displayed()

    def is_heading_description_visible(self):
        return self.driver.find_element(*self.heading_description).is_displayed()

    def get_contact_page_title_text(self):
        return self.driver.find_element(*self.contact_page_title).text

    def get_heading_description_text(self):
        return self.driver.find_element(*self.heading_description).text

    def is_success_message_visible(self):
        wait = WebDriverWait(self.driver, 30)
        message = wait.until(EC.visibility_of_element_located(self.success_message))
        return message.is_displayed()

    def set_name_field(self, name):
        self.driver.find_element(*self.name_input_field).clear()
        self.driver.find_element(*self.name_input_field).send_keys(name)

    def set_email_field(self, email):
        self.driver.find_element(*self.email_input_field).clear()
        self.driver.find_element(*self.email_input_field).send_keys(email)

    def set_message_field(self, message):
        self.driver.find_element(*self.message_input_field).clear()
        self.driver.find_element(*self.message_input_field).send_keys(message)

    def click_send_message_button(self):
        self.driver.find_element(*self.send_message_button).click()

    def is_message_section_visible(self):
        return self.driver.find_element(*self.message_section).is_displayed()

    def is_details_section_visible(self):
        return self.driver.find_element(*self.details_section).is_displayed()

    def is_transport_section_visible(self):
        return self.driver.find_element(*self.transport_section).is_displayed()

    def is_footer_visible(self):
        return self.driver.find_element(*self.footer).is_displayed()

    def scroll_to_transport_section(self, browser):
        element = self.driver.find_element(*self.transport_section)
        BaseClass.scroll_to_element(self.driver, element, browser)

    def scroll_to_message_section(self, browser):
        element = self.driver.find_element(*self.message_section)
        BaseClass.scroll_to_element(self.driver, element, browser)

    def is_name_field_visible(self):
        return self.driver.find_element(*self.name_input_field).is_displayed()

    def get_name_field_placeholder(self):
        return self.driver.find_element(*self.name_input_field).get_attribute("placeholder")

    def get_name_field_value(self):
        return self.driver.find_element(*self.name_input_field).get_attribute("value")

    def is_email_field_visible(self):
        return self.driver.find_element(*self.email_input_field).is_displayed()

    def get_email_field_placeholder(self):
        return self.driver.find_element(*self.email_input_field).get_attribute("placeholder")

    def get_email_field_value(self):
        return self.driver.find_element(*self.email_input_field).get_attribute("value")

    def is_invalid_email_error_visible(self):
        return self.driver.find_element(*self.invalid_email_error).is_displayed()

    def get_invalid_email_error_text(self):
        return self.driver.find_element(*self.invalid_email_error).text

    def is_message_field_visible(self):
        return self.driver.find_element(*self.message_input_field).is_displayed()

    def get_message_field_placeholder(self):
        return self.driver.find_element(*self.message_input_field).get_attribute("placeholder")

    def get_message_field_value(self):
        return self.driver.find_element(*self.message_input_field).get_attribute("value")

    def is_details_element_visible(self, title):
        return self.driver.find_element(By.XPATH, f"//aside//h3[.='{title}']").is_displayed()

    def get_details_element_text(self, title):
        detail_text = ""
        elements = self.driver.find_elements(By.XPATH, f"//aside//h3[.='{title}']/../p")
        for element in elements:
            detail_text = detail_text + element.text.strip()
        return detail_text

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





