import os
import re
import time
import pytz
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SponsorsPage:

    def __init__(self, driver):
        self.driver = driver
        self.heading_title = (By.XPATH, "//h1")
        self.heading_description = (By.XPATH, "//div[@class='page-heading']/div/div")
        self.sponsor_cards = (By.XPATH, "//div[@class='sponsor-card']")
        self.get_involved_title = (By.XPATH, "//div[@class='get-involved']//h2")
        self.get_involved_description = (By.XPATH, "//div[@class='get-involved-heading']/div")
        self.get_involved_button = (By.XPATH, "//div[@class='get-involved-heading']//a")
        self.benefits_section = (By.XPATH, "//div[@class='get-involved-benefits']")
        self.benefits_title = (By.XPATH, "//div[@class='get-involved-benefits']//h3")
        self.benefits_description = (By.XPATH, "//div[@class='get-involved-benefits']//div[@class='description']")

    def is_sponsors_page_title_visible(self, title):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[.='{title}']")))
        return page_title.is_displayed()

    def get_heading_title_text(self):
        return self.driver.find_element(*self.heading_title).text

    def is_heading_title_visible(self):
        return self.driver.find_element(*self.heading_title).is_displayed()

    def get_heading_description_text(self):
        return self.driver.find_element(*self.heading_description).text.strip()

    def is_heading_description_visible(self):
        return self.driver.find_element(*self.heading_description).is_displayed()

    def get_sponsor_cards_number(self):
        cards = self.driver.find_elements(*self.sponsor_cards)
        return len(cards)

    def sponsor_cards_are_images(self):
        cards = self.driver.find_elements(*self.sponsor_cards)
        cond = True
        for card in cards:
            if not card.find_element(By.XPATH, "./img").is_displayed():
                cond = False
        return cond

    def get_sponsors_card_image(self, num):
        cards = self.driver.find_elements(*self.sponsor_cards)
        file_name = cards[num].find_element(By.XPATH, "./img").get_attribute('src')
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', file_name)
        if filename:
            filename = filename.group(0)
        return filename.replace("%20", " ")

    def is_get_involved_title_visible(self):
        return self.driver.find_element(*self.get_involved_title).is_displayed()

    def is_get_involved_description_visible(self):
        return self.driver.find_element(*self.get_involved_description).is_displayed()

    def is_get_involved_button_visible(self):
        return self.driver.find_element(*self.get_involved_button).is_displayed()

    def get_get_involved_button_text(self):
        return self.driver.find_element(*self.get_involved_button).text.strip()

    def click_get_involved_button(self):
        self.driver.find_element(*self.get_involved_button).click()

    def is_benefits_section_visible(self):
        return self.driver.find_element(*self.benefits_section).is_displayed()

    def get_get_involved_title_text(self):
        return self.driver.find_element(*self.get_involved_title).text.strip()

    def get_get_involved_description_text(self):
        description = self.driver.find_element(*self.get_involved_description).text
        return description.replace("<br>", "").replace("\n", "").strip()

    def scroll_to_benefits_section(self, browser):
        element = self.driver.find_element(*self.benefits_section)
        self.scroll_to_element(element, browser)

    def are_benefits_titles_visible(self):
        elements = self.driver.find_elements(*self.benefits_title)
        if len(elements) > 0:
            return True
        else:
            return False

    def are_benefits_descriptions_visible(self):
        elements = self.driver.find_elements(*self.benefits_description)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_benefits_title_text(self):
        titles = []
        elements = self.driver.find_elements(*self.benefits_title)
        for element in elements:
            titles.append(element.text.strip())
        return titles

    def get_benefits_description_text(self):
        descriptions = []
        description = ""
        elements = self.driver.find_elements(*self.benefits_description)
        for element in elements:
            paragraphs = element.find_elements(By.XPATH, ".//p")
            for paragraph in paragraphs:
                description = description + paragraph.text.strip()
            descriptions.append(description)
            description = ""
        return descriptions

    def get_benefits_elements_number(self):
        elements = self.driver.find_elements(*self.benefits_title)
        return len(elements)

    def scroll_to_element(self, element, browser):
        location = element.location
        x = location['x']
        y = location['y']
        if browser == 'safari':
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

