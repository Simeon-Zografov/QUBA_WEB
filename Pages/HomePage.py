import os
import re
import time
import pytz
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class HomePage:

    def __init__(self, driver):
        self.driver = driver
        self.hero_banner = (By.XPATH, "//section[@class='app-hero']")
        self.app_download_section = (By.XPATH, "//section[@class='app-download']")
        self.site_carousel_section = (By.XPATH, "(//section[@class='container'])[1]")
        self.event_carousel_section = (By.XPATH, "(//section[@class='container'])[2]")
        self.app_footer = (By.XPATH, "//div[@class='app-footer']")
        self.hero_banner_title = (By.XPATH, "//h1")
        self.hero_banner_subtitle = (By.XPATH, "//h1/..//p")
        self.hero_banner_button = (By.XPATH, "//h1/..//a")
        self.download_title = (By.XPATH, "//section[@class='app-download']//h2")
        self.download_description = (By.XPATH, "//section[@class='app-download']//p")
        self.download_image = (By.XPATH, "//section[@class='app-download']//div/img")
        self.download_stats_section = (By.XPATH, "//section[@class='app-download']//ul")
        self.download_stat_value = (By.XPATH, "//section[@class='app-download']//li/strong")
        self.download_stat_description = (By.XPATH, "//section[@class='app-download']//li/span")
        self.download_google_button = (By.XPATH, "//section[@class='app-download']//a[contains(@href, 'google')]")
        self.download_apple_button = (By.XPATH, "//section[@class='app-download']//a[contains(@href, 'apple')]")
        self.site_carousel_title = (By.XPATH, "(//section[@class='container'])[1]//h2")
        self.site_carousel_description = (By.XPATH, "(//section[@class='container'])[1]//div[@class='description']")
        self.site_carousel_link = (By.XPATH, "(//section[@class='container'])[1]//a[@class='icon-text']")
        self.site_carousel_card = (By.XPATH, "(//section[@class='container'])[1]//div[@class='card app-carousel-card']")
        self.site_carousel_card_titles = (By.XPATH, "(//section[@class='container'])[1]//div[@id='carousel']//h4")
        self.site_carousel_card_descriptions = (By.XPATH, "(//section[@class='container'])[1]//div[@id='carousel']//p")
        self.site_carousel_card_images = (By.XPATH, "(//section[@class='container'])[1]//div[@id='carousel']//img")
        self.event_carousel_title = (By.XPATH, "(//section[@class='container'])[2]//h2")
        self.event_carousel_description = (By.XPATH, "(//section[@class='container'])[2]//div[@class='description']")
        self.event_carousel_link = (By.XPATH, "(//section[@class='container'])[2]//a[@class='icon-text']")
        self.event_carousel_card = (By.XPATH, "(//section[@class='container'])[2]//div[@class='card app-carousel-card']")
        self.event_carousel_card_titles = (By.XPATH, "(//section[@class='container'])[2]//div[@id='carousel']//h4")
        self.event_carousel_card_descriptions = (By.XPATH, "(//section[@class='container'])[2]//div[@id='carousel']//p")
        self.event_carousel_card_images = (By.XPATH, "(//section[@class='container'])[2]//div[@id='carousel']//img")
        self.event_carousel_card_time = (By.XPATH, "(//section[@class='container'])[2]//div[@class='card-footer']")

    def is_home_page_title_visible(self, title):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[.='{title}']")))
        return page_title.is_displayed()

    def is_hero_banner_visible(self):
        return self.driver.find_element(*self.hero_banner).is_displayed()

    def is_app_download_section_visible(self):
        return self.driver.find_element(*self.app_download_section).is_displayed()

    def is_site_carousel_section_visible(self):
        return self.driver.find_element(*self.site_carousel_section).is_displayed()

    def is_event_carousel_section_visible(self):
        return self.driver.find_element(*self.event_carousel_section).is_displayed()

    def is_app_footer_visible(self):
        return self.driver.find_element(*self.app_footer).is_displayed()

    def is_hero_banner_title_visible(self):
        return self.driver.find_element(*self.hero_banner_title).is_displayed()

    def get_hero_banner_title_text(self):
        return self.driver.find_element(*self.hero_banner_title).text

    def is_hero_banner_subtitle_visible(self):
        return self.driver.find_element(*self.hero_banner_subtitle).is_displayed()

    def get_hero_banner_subtitle_text(self):
        return self.driver.find_element(*self.hero_banner_subtitle).text

    def is_hero_banner_button_visible(self):
        return self.driver.find_element(*self.hero_banner_button).is_displayed()

    def get_hero_banner_button_text(self):
        return self.driver.find_element(*self.hero_banner_button).text

    def click_hero_banner_button(self):
        self.driver.find_element(*self.hero_banner_button).click()

    def get_hero_banner_image(self):
        image = self.driver.find_element(*self.hero_banner).get_attribute("style")
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', image)
        if filename:
            filename = filename.group(0)
        return filename.replace("\\", "")

    def is_download_title_visible(self):
        return self.driver.find_element(*self.download_title).is_displayed()

    def get_download_title_text(self):
        return self.driver.find_element(*self.download_title).text

    def is_download_description_visible(self):
        elements = self.driver.find_elements(*self.download_description)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_download_description_text(self):
        description_text = ""
        elements = self.driver.find_elements(*self.download_description)
        for element in elements:
            description_text = description_text + element.text.strip()
        return description_text

    def is_download_image_visible(self):
        return self.driver.find_element(*self.download_image).is_displayed()

    def get_download_image(self):
        image = self.driver.find_element(*self.download_image).get_attribute("src")
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', image)
        if filename:
            filename = filename.group(0)
        return filename

    def is_download_stats_section_visible(self):
        return self.driver.find_element(*self.download_stats_section).is_displayed()

    def get_download_stats(self, num):
        values = self.driver.find_elements(*self.download_stat_value)
        descriptions = self.driver.find_elements(*self.download_stat_description)
        value = values[num].text
        description = descriptions[num].text
        return value, description

    def get_stats_pairs_number(self):
        values = self.driver.find_elements(*self.download_stat_value)
        return len(values)

    def is_download_google_play_button_visible(self):
        return self.driver.find_element(*self.download_google_button).is_displayed()

    def get_download_google_play_button_url(self):
        return self.driver.find_element(*self.download_google_button).get_attribute('href')

    def is_download_app_store_button_visible(self):
        return self.driver.find_element(*self.download_apple_button).is_displayed()

    def get_download_app_store_button_url(self):
        return self.driver.find_element(*self.download_apple_button).get_attribute('href')

    def is_site_carousel_title_visible(self):
        return self.driver.find_element(*self.site_carousel_title).is_displayed()

    def get_site_carousel_title_text(self):
        return self.driver.find_element(*self.site_carousel_title).text

    def is_site_carousel_description_visible(self):
        return self.driver.find_element(*self.site_carousel_description).is_displayed()

    def get_site_carousel_description_text(self):
        return self.driver.find_element(*self.site_carousel_description).text

    def is_site_carousel_button_visible(self):
        return self.driver.find_element(*self.site_carousel_link).is_displayed()

    def get_site_carousel_button_text(self):
        return self.driver.find_element(*self.site_carousel_link).text

    def click_site_carousel_button(self):
        element = self.driver.find_element(*self.site_carousel_link)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def is_site_carousel_cards_visible(self):
        elements = self.driver.find_elements(*self.site_carousel_card_titles)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_site_carousel_cards_number(self):
        elements = self.driver.find_elements(*self.site_carousel_card_titles)
        return len(elements)

    def get_site_carousel_card_title(self, num):
        card_titles = self.driver.find_elements(*self.site_carousel_card_titles)
        card_title = card_titles[num].text
        return card_title

    def get_site_carousel_card_description(self, num):
        card_descriptions = self.driver.find_elements(*self.site_carousel_card_descriptions)
        card_description = card_descriptions[num].text
        return card_description

    def get_site_carousel_card_image(self, num):
        card_images = self.driver.find_elements(*self.site_carousel_card_images)
        card_image = card_images[num].get_attribute('src')
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', card_image)
        if filename:
            filename = filename.group(0)
        return filename.replace("%20", " ")

    def click_site_carousel_card(self, num):
        cards = self.driver.find_elements(*self.site_carousel_card)
        element = cards[num]
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def is_event_carousel_title_visible(self):
        return self.driver.find_element(*self.event_carousel_title).is_displayed()

    def get_event_carousel_title_text(self):
        return self.driver.find_element(*self.event_carousel_title).text

    def is_event_carousel_description_visible(self):
        return self.driver.find_element(*self.event_carousel_description).is_displayed()

    def get_event_carousel_description_text(self):
        return self.driver.find_element(*self.event_carousel_description).text

    def is_event_carousel_button_visible(self):
        return self.driver.find_element(*self.event_carousel_link).is_displayed()

    def get_event_carousel_button_text(self):
        return self.driver.find_element(*self.event_carousel_link).text

    def click_event_carousel_button(self):
        element = self.driver.find_element(*self.event_carousel_link)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def is_event_carousel_cards_visible(self):
        elements = self.driver.find_elements(*self.event_carousel_card_titles)
        if len(elements) > 0:
            return True
        else:
            return False

    def get_event_carousel_cards_number(self):
        elements = self.driver.find_elements(*self.event_carousel_card_titles)
        return len(elements)

    def get_event_carousel_card_title(self, num):
        card_titles = self.driver.find_elements(*self.event_carousel_card_titles)
        card_title = card_titles[num].text
        return card_title

    def get_event_carousel_card_description(self, num):
        card_descriptions = self.driver.find_elements(*self.event_carousel_card_descriptions)
        card_description = card_descriptions[num].text
        return card_description

    def get_event_carousel_card_image(self, num):
        card_images = self.driver.find_elements(*self.event_carousel_card_images)
        card_image = card_images[num].get_attribute('src')
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', card_image)
        if filename:
            filename = filename.group(0)
        return filename.replace("%20", " ")

    def click_event_carousel_card(self, num):
        cards = self.driver.find_elements(*self.event_carousel_card)
        element = cards[num]
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def get_event_carousel_card_time(self, num):
        card_times = self.driver.find_elements(*self.event_carousel_card_time)
        card_time = card_times[num].text
        return card_time
