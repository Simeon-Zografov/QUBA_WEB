import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Events:

    def __init__(self, driver):
        self.driver = driver
        self.sites_page_title = (By.XPATH, "//h1[.='Events that shape tomorrow']")
        self.individual_event_title = (By.XPATH, "//h1")
        self.back_button = (By.XPATH, "//a[@class='back-link icon-text']")

    def get_individual_event_title_text(self):
        return self.driver.find_element(*self.individual_event_title).text

    def wait_individual_event_page_to_load(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located(self.back_button))
