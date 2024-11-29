import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AboutPage:

    def __init__(self, driver):
        self.driver = driver
        self.heading = (By.XPATH, "//div[@class='page-heading']")
        self.themes_section = (By.XPATH, "//div[@class='themes']")
        self.image_gallery = (By.XPATH, "//div[@class='image-gallery']")
        self.faq_section = (By.XPATH, "//div[@class='faq']")
        self.transport_section = (By.XPATH, "//section[@class='site-travel-info']")
        self.heading_title = (By.XPATH, "//h1")
        self.heading_description = (By.XPATH, "//div[@class='page-heading']/div/div")
        self.themes_title = (By.XPATH, "//div[@class='themes']//h2")
        self.themes_description = (By.XPATH, "//div[@class='themes']//header//div[@class='description']")
        self.theme_cards = (By.XPATH, "//div[@class='theme-card']")
        self.theme_card_title = (By.XPATH, "//div[@class='theme-card']//h3")
        self.theme_card_description = (By.XPATH, "//div[@class='theme-card']//div[@class='description']")
        self.next_slide_button = (By.XPATH, "//button[@class='next-slide']")
        self.previous_slide_button = (By.XPATH, "//button[@class='prev-slide']")
        self.image_carousel = (By.XPATH, "//div[@class='slide-container']")
        self.single_image = (By.XPATH, "//div[@class='slide-container']/img")
        self.faq_title = (By.XPATH, "//div[@id='faq']//h2")
        self.faq_description = (By.XPATH, "//div[@id='faq']//div[@class='description']")
        self.faq_element = (By.XPATH, "//dl[@class='frequently-asked-question']")
        self.faq_element_question = (By.XPATH, "//dl[@class='frequently-asked-question']/dt")
        self.faq_element_answer = (By.XPATH, "//dl[@class='frequently-asked-question']/dd")
        self.public_transport_card = (By.XPATH, "//div[@class='card info-panel public-transport']")
        self.parking_card = (By.XPATH, "//div[@class='card info-panel parking']")
        self.taxi_card = (By.XPATH, "//div[@class='card info-panel taxi']")
        self.transport_card_title = (By.XPATH, "//div[contains(@class, 'card info-panel')]//h4")
        self.transport_card_description = (By.XPATH, "//div[contains(@class, 'card info-panel')]//p")
        self.public_transport_card_link = (By.XPATH, "//div[@class='card info-panel public-transport']//a")
        self.parking_card_link = (By.XPATH, "//div[@class='card info-panel parking']//a")
        self.taxi_card_link = (By.XPATH, "//div[@class='card info-panel taxi']//a")
        self.cards_titles = ["Public transport", "Parking", "Taxis"]
        self.card_descriptions = ["The site is accessible by public transport.", "There is parking available at the site.",
                                  "Taxis are available to and from the site."]

    def is_about_page_title_visible(self, title):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[.='{title}']")))
        return page_title.is_displayed()

    def is_heading_visible(self):
        return self.driver.find_element(*self.heading).is_displayed()

    def is_themes_section_visible(self):
        return self.driver.find_element(*self.themes_section).is_displayed()

    def is_image_gallery_visible(self):
        return self.driver.find_element(*self.image_gallery).is_displayed()

    def is_faq_section_visible(self):
        return self.driver.find_element(*self.faq_section).is_displayed()

    def is_transport_section_visible(self, browser):
        element = self.driver.find_element(*self.transport_section)
        self.scroll_to_element(element, browser)
        return element.is_displayed()

    def get_heading_title_text(self):
        return self.driver.find_element(*self.heading_title).text

    def get_heading_description_text(self):
        return self.driver.find_element(*self.heading_description).text

    def get_themes_title_text(self):
        return self.driver.find_element(*self.themes_title).text

    def is_themes_title_visible(self):
        return self.driver.find_element(*self.themes_title).is_displayed()

    def get_themes_description_text(self):
        return self.driver.find_element(*self.themes_description).text

    def is_themes_description_visible(self):
        return self.driver.find_element(*self.themes_description).is_displayed()

    def get_theme_cards_number(self):
        elements = self.driver.find_elements(*self.theme_cards)
        return len(elements)

    def get_theme_card_title(self, num):
        card_titles = self.driver.find_elements(*self.theme_card_title)
        title = card_titles[num].text
        return title

    def get_theme_card_description(self, num):
        description_text = ""
        card_descriptions = self.driver.find_elements(*self.theme_card_description)
        description = card_descriptions[num]
        paragraphs = description.find_elements(By.XPATH, ".//p")
        for paragraph in paragraphs:
            description_text = description_text + paragraph.text.strip()
        description_text = str(re.sub(' +', ' ', description_text))
        return description_text.strip()

    def click_next_slide_button(self):
        self.driver.find_element(*self.next_slide_button).click()
        time.sleep(1)

    def is_next_slide_button_visible(self):
        time.sleep(1)
        elements = self.driver.find_elements(*self.next_slide_button)
        if len(elements) > 0:
            return True
        else:
            return False

    def click_previous_slide_button(self):
        self.driver.find_element(*self.previous_slide_button).click()
        time.sleep(1)

    def is_previous_slide_button_visible(self):
        time.sleep(1)
        elements = self.driver.find_elements(*self.previous_slide_button)
        if len(elements) > 0:
            return True
        else:
            return False

    def is_image_carousel_scroll_visible(self):
        scroll_width = self.driver.find_element(*self.image_carousel).get_attribute('scrollWidth')
        offset_width = self.driver.find_element(*self.image_carousel).get_attribute('offsetWidth')
        if scroll_width > offset_width:
            return True
        else:
            return False

    def get_image_carousel_position(self):
        carousel = self.driver.find_element(*self.image_carousel)
        container = carousel.find_element(By.XPATH, "..")
        container_class = container.get_attribute('class')
        if "is-first" in container_class:
            return "start"
        elif "is-last" in container_class:
            return "end"
        else:
            return "middle"

    def get_images(self):
        images_list = []
        images = self.driver.find_elements(*self.single_image)
        for image in images:
            file_name = image.get_attribute('src')
            filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', file_name)
            if filename:
                filename = filename.group(0)
            images_list.append(filename.replace("%20", " "))
        return images_list

    def scroll_to_image_gallery(self, browser):
        element = self.driver.find_element(*self.image_carousel)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='slide-container']"))
        )
        self.scroll_to_element(element, browser)

    def scroll_right_in_image_gallery(self):
        element = self.driver.find_element(*self.image_carousel)
        self.driver.execute_script("arguments[0].scrollBy({ top: 0, left: 500, behavior: 'smooth' });", element)
        time.sleep(1)

    def scroll_left_in_image_gallery(self):
        element = self.driver.find_element(*self.image_carousel)
        self.driver.execute_script("arguments[0].scrollBy({ top: 0, left: -500, behavior: 'smooth' });", element)
        time.sleep(1)

    def get_faq_title_text(self):
        return self.driver.find_element(*self.faq_title).text

    def is_faq_title_visible(self):
        return self.driver.find_element(*self.faq_title).is_displayed()

    def get_faq_description_text(self):
        return self.driver.find_element(*self.faq_description).text

    def is_faq_description_visible(self):
        return self.driver.find_element(*self.faq_description).is_displayed()

    def are_faq_elements_visible(self):
        elements = self.driver.find_elements(*self.faq_element)
        if len(elements) == 0:
            return False
        else:
            return True

    def get_faq_elements_number(self):
        elements = self.driver.find_elements(*self.faq_element)
        return len(elements)

    def click_faq_element(self, num, browser):
        elements = self.driver.find_elements(*self.faq_element_question)
        self.scroll_to_element(elements[num], browser)
        elements[num].click()
        time.sleep(0.5)

    def is_faq_element_expanded(self, num):
        elements = self.driver.find_elements(*self.faq_element_question)
        element = elements[num]
        element_attribute = element.get_attribute('aria-expanded')
        if element_attribute == "true":
            return True
        else:
            return False

    def get_faq_element_question(self, num):
        elements = self.driver.find_elements(*self.faq_element_question)
        element = elements[num]
        return element.text

    def get_faq_element_answer(self, num):
        answer_text = ""
        element_answers = self.driver.find_elements(*self.faq_element_answer)
        answer = element_answers[num]
        paragraphs = answer.find_elements(By.XPATH, ".//p")
        for paragraph in paragraphs:
            answer_text = answer_text + paragraph.text.strip()
        description_text = str(re.sub(' +', ' ', answer_text))
        return description_text.strip()

    def scroll_to_faq_section(self, browser):
        element = self.driver.find_element(*self.faq_section)
        self.scroll_to_element(element, browser)

    def scroll_to_transport_section(self, browser):
        element = self.driver.find_element(*self.transport_section)
        self.scroll_to_element(element, browser)

    def is_public_transport_card_visible(self):
        return self.driver.find_element(*self.public_transport_card).is_displayed()

    def is_parking_card_visible(self):
        return self.driver.find_element(*self.parking_card).is_displayed()

    def is_taxi_card_visible(self):
        return self.driver.find_element(*self.taxi_card).is_displayed()

    def get_transport_cards_title(self, num):
        elements = self.driver.find_elements(*self.transport_card_title)
        return elements[num].text

    def get_transport_cards_description(self, num):
        elements = self.driver.find_elements(*self.transport_card_description)
        return elements[num].text

    def click_public_transport_card_link(self):
        self.driver.find_element(*self.public_transport_card_link).click()

    def click_parking_card_link(self):
        self.driver.find_element(*self.parking_card_link).click()

    def click_taxi_card_link(self):
        self.driver.find_element(*self.taxi_card_link).click()

    def scroll_to_element(self, element, browser):
        location = element.location
        x = location['x']
        y = location['y']
        if browser == 'safari':
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
