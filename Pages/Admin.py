import re
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from Common.BaseClass import BaseClass


class Admin:

    def __init__(self, driver):
        self.driver = driver
        self.email_field = (By.NAME, "email")
        self.password_field = (By.NAME, "password")
        self.login_button = (By.XPATH, "//button[@type='submit']")
        self.content_manager_button = (By.XPATH, "(//span[.='Content Manager'])[1]/..")
        self.home_page_button = (By.XPATH, "//span[.='Home page']/../../..")
        self.hero_title = (By.ID, "hero.title")
        self.hero_subtitle = (By.ID, "hero.subtitle")
        self.hero_image = (By.XPATH, "//label[contains(., 'coverImage')]/..//span[@class='sc-dkPtRN cSldSA']")
        self.hero_link_text = (By.ID, "hero.link.text")
        self.hero_link_url = (By.ID, "hero.link.url")
        self.download_title = (By.ID, "download.title")
        self.download_description = (By.XPATH, "//label[contains(., 'download')]/../../..//p//span[@data-slate-string='true']")
        self.download_image = (By.XPATH, "//label[contains(., 'showcase')]/../../..//span[@class='sc-dkPtRN cSldSA']")
        self.download_stats_button = (By.XPATH, "//button[@class='sc-bdvvtL sc-gsDKAQ sc-fWCJzd exHuNB kpZefO eJIDkS sc-eXlEPa gfLTwt']")
        self.site_carousel_title = (By.ID, "siteCarousel.sectionTitle.title")
        self.site_carousel_description = (By.XPATH, "//label[contains(., 'siteCarousel')]/../../..//textarea")
        self.site_carousel_link_text = (By.ID, "siteCarousel.sectionTitle.linkText")
        self.site_carousel_link_url = (By.ID, "siteCarousel.sectionTitle.linkUrl")
        self.site_carousel_site_name = (By.XPATH, "//label[contains(., 'siteCarousel')]/../../..//a/span")
        self.event_carousel_title = (By.ID, "eventCarousel.sectionTitle.title")
        self.event_carousel_description = (By.XPATH, "//label[contains(., 'eventCarousel')]/../../..//textarea")
        self.event_carousel_link_text = (By.ID, "eventCarousel.sectionTitle.linkText")
        self.event_carousel_link_url = (By.ID, "eventCarousel.sectionTitle.linkUrl")
        self.about_page_button = (By.XPATH, "//span[.='About page']/../../..")
        self.about_heading_title = (By.ID, "heading.title")
        self.about_heading_description = (By.XPATH, "//label[contains(., 'heading')]/../../..//textarea")
        self.about_themes_title = (By.ID, "themes.sectionTitle.title")
        self.about_themes_description = (By.XPATH, "//label[contains(., 'themes')]/../../..//textarea")
        self.about_themes_buttons = (By.XPATH, "//button[contains(@aria-controls, 'accordion-content-themes.themes')]")
        self.about_theme_title = (By.XPATH, "//input[contains(@id, 'themes.themes') and @aria-required='true']")
        self.about_theme_description = (By.XPATH, "//label[contains(., 'themes')]/../../..//div["
                                                  "@role='textbox']//p//span[@data-slate-string='true']")
        self.about_image_gallery_title = (By.ID, "imageGallery.sectionTitle.title")
        self.about_image_gallery_description = (By.ID, "imageGallery.sectionTitle.description")
        self.about_image_gallery_image = (By.XPATH, "//label[contains(., 'imageGallery')]/../../..//span[@class='sc-dkPtRN "
                                              "cSldSA']")
        self.about_next_image_button = (By.XPATH, "//button[@aria-label='Next slide']")
        self.about_faq_title = (By.ID, "faq.sectionTitle.title")
        self.about_faq_description = (By.XPATH, "//label[contains(., 'faq')]/../../..//textarea")
        self.about_faq_buttons = (By.XPATH, "//button[contains(@aria-controls, 'accordion-content-faq')]")
        self.about_single_faq_title = (By.XPATH, "//input[contains(@id, 'faq.FAQ')]")
        self.about_single_faq_description = (By.XPATH, "//label[contains(., 'FAQ')]/../../..//div["
                                                       "@role='textbox']//p//span[@data-slate-string='true']")

    def set_email(self):
        self.driver.find_element(*self.email_field).clear()
        self.driver.find_element(*self.email_field).send_keys(BaseClass.cms_email)

    def set_password(self):
        self.driver.find_element(*self.password_field).clear()
        self.driver.find_element(*self.password_field).send_keys(BaseClass.cms_password)

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def switch_to_admin(self):
        self.driver.switch_to.new_window('tab')
        self.driver.get(BaseClass.cms_url)
        self.set_email()
        self.set_password()
        self.click_login_button()

    def close_admin(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
        time.sleep(1)

    def click_content_manager_button(self):
        self.driver.find_element(*self.content_manager_button).click()

    def click_home_page_button(self):
        self.driver.find_element(*self.home_page_button).click()

    def get_hero_title_value(self):
        return self.driver.find_element(*self.hero_title).get_attribute('value')

    def get_hero_subtitle_value(self):
        return self.driver.find_element(*self.hero_subtitle).get_attribute('value')

    def get_hero_link_text(self):
        return self.driver.find_element(*self.hero_link_text).get_attribute('value')

    def get_hero_link_url(self):
        return self.driver.find_element(*self.hero_link_url).get_attribute('value')

    def get_hero_image(self):
        return self.driver.find_element(*self.hero_image).text

    def get_download_title_text(self):
        return self.driver.find_element(*self.download_title).get_attribute('value')

    def get_download_description_text(self):
        description_text = ""
        elements = self.driver.find_elements(*self.download_description)
        for element in elements:
            description_text = description_text + element.text.strip()
        return description_text

    def get_download_image(self):
        return self.driver.find_element(*self.download_image).text

    def get_download_stats(self):
        stats = {}
        i = 0
        elements = self.driver.find_elements(*self.download_stats_button)
        for element in elements:
            element.click()
            stat = self.driver.find_element(By.ID, f"download.stats.{i}.value").get_attribute('value')
            description = self.driver.find_element(By.ID, f"download.stats.{i}.description").get_attribute('value')
            stats[stat] = description
            i = i + 1
        return stats

    def get_site_carousel_title_text(self):
        return self.driver.find_element(*self.site_carousel_title).get_attribute('value')

    def get_site_carousel_description_text(self):
        return self.driver.find_element(*self.site_carousel_description).text

    def get_site_carousel_link_text(self):
        return self.driver.find_element(*self.site_carousel_link_text).get_attribute('value')

    def get_site_carousel_link_url(self):
        return self.driver.find_element(*self.site_carousel_link_url).get_attribute('value')

    def get_site_carousel_sites(self):
        sites = {}
        i = 0
        elements = self.driver.find_elements(*self.site_carousel_site_name)
        for element in elements:
            sites[i] = element.text
            i = i + 1
        return sites

    def get_event_carousel_title_text(self):
        return self.driver.find_element(*self.event_carousel_title).get_attribute('value')

    def get_event_carousel_description_text(self):
        return self.driver.find_element(*self.event_carousel_description).text

    def get_event_carousel_link_text(self):
        return self.driver.find_element(*self.event_carousel_link_text).get_attribute('value')

    def get_event_carousel_link_url(self):
        return self.driver.find_element(*self.event_carousel_link_url).get_attribute('value')

    def get_home_page_content(self):
        self.click_content_manager_button()
        self.click_home_page_button()
        content = {
            "hero_title": self.get_hero_title_value(),
            "hero_subtitle": self.get_hero_subtitle_value(),
            "hero_image": self.get_hero_image(),
            "hero_link_text": self.get_hero_link_text(),
            "hero_link_url": self.get_hero_link_url(),
            "download_title": self.get_download_title_text(),
            "download_description": self.get_download_description_text(),
            "download_image": self.get_download_image(),
            "download_stats": self.get_download_stats(),
            "site_carousel_title": self.get_site_carousel_title_text(),
            "site_carousel_description": self.get_site_carousel_description_text(),
            "site_carousel_link_text": self.get_site_carousel_link_text(),
            "site_carousel_link_url": self.get_site_carousel_link_url(),
            "site_carousel_sites": self.get_site_carousel_sites(),
            "event_carousel_title": self.get_event_carousel_title_text(),
            "event_carousel_description": self.get_event_carousel_description_text(),
            "event_carousel_link_text": self.get_event_carousel_link_text(),
            "event_carousel_link_url": self.get_event_carousel_link_url()
        }
        return content

    def click_about_page_button(self):
        self.driver.find_element(*self.about_page_button).click()

    def get_about_heading_title_value(self):
        return self.driver.find_element(*self.about_heading_title).get_attribute('value')

    def get_about_heading_description_text(self):
        description_text = ""
        elements = self.driver.find_elements(*self.about_heading_description)
        for element in elements:
            description_text = description_text + element.text.strip()
        return description_text

    def get_about_themes_title_value(self):
        return self.driver.find_element(*self.about_themes_title).get_attribute('value')

    def get_about_themes_description_text(self):
        description_text = ""
        elements = self.driver.find_elements(*self.about_themes_description)
        for element in elements:
            description_text = description_text + element.text.strip()
        return description_text

    def get_about_themes_elements(self):
        content = {}
        description_text = ""
        elements = self.driver.find_elements(*self.about_themes_buttons)
        for element in elements:
            element.click()
            title = self.driver.find_element(*self.about_theme_title).get_attribute('value')
            paragraphs = self.driver.find_elements(*self.about_theme_description)
            for paragraph in paragraphs:
                description_text = description_text + paragraph.text.strip()
            description_text = str(re.sub(' +', ' ', description_text))
            content[title] = description_text
            description_text = ""
        return content

    def get_image_gallery_title_value(self):
        return self.driver.find_element(*self.about_image_gallery_title).get_attribute('value')

    def get_image_gallery_description_text(self):
        return self.driver.find_element(*self.about_image_gallery_description).text

    def click_next_slide_button(self):
        self.driver.find_element(*self.about_next_image_button).click()

    def get_image_gallery_image(self):
        return self.driver.find_element(*self.about_image_gallery_image).text

    def get_gallery_images(self):
        first_image = self.get_image_gallery_image()
        images = []
        while True:
            images.append(self.get_image_gallery_image())
            self.click_next_slide_button()
            if first_image == self.get_image_gallery_image():
                break
        return images

    def get_faq_title_value(self):
        return self.driver.find_element(*self.about_faq_title).get_attribute('value')

    def get_faq_description_text(self):
        return self.driver.find_element(*self.about_faq_description).text

    def get_faq_elements(self):
        content = {}
        description_text = ""
        elements = self.driver.find_elements(*self.about_faq_buttons)
        for element in elements:
            element.click()
            title = self.driver.find_element(*self.about_single_faq_title).get_attribute('value')
            paragraphs = self.driver.find_elements(*self.about_single_faq_description)
            for paragraph in paragraphs:
                description_text = description_text + paragraph.text.strip()
            description_text = str(re.sub(' +', ' ', description_text))
            content[title] = description_text
            description_text = ""
        return content

    def get_about_page_content(self):
        self.click_content_manager_button()
        self.click_about_page_button()
        content = {
            "heading_title": self.get_about_heading_title_value(),
            "heading_description": self.get_about_heading_description_text(),
            "themes_title": self.get_about_themes_title_value(),
            "themes_description": self.get_about_themes_description_text(),
            "theme_elements": self.get_about_themes_elements(),
            "gallery_title": self.get_image_gallery_title_value(),
            "gallery_description": self.get_image_gallery_description_text(),
            "gallery_images": self.get_gallery_images(),
            "faq_title": self.get_faq_title_value(),
            "faq_description": self.get_faq_description_text(),
            "faq_elements": self.get_faq_elements()
        }
        return content
