import os
import re
import time
from datetime import datetime
import pytz
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Events:

    def __init__(self, driver):
        self.driver = driver
        self.events_page_title = (By.XPATH, "//h1")
        self.page_title_by_title = "//h1[contains(., '{title}')]"
        self.heading_description = (By.XPATH, "//div[@class='heading-top']//div")
        self.section_title = (By.XPATH, "//header[@class='section-heading']/h2")
        self.section_description = (By.XPATH, "//header[@class='section-heading']/div")
        self.individual_event_title = (By.XPATH, "//h1")
        self.back_button = (By.XPATH, "//a[@class='back-link icon-text']")
        self.event_card = (By.XPATH, "//div[@class='card-body']")
        self.event_section = (By.ID, "carousel")
        self.pagination = (By.XPATH, "//ul[@aria-label='Pagination']")
        self.go_to_next_page = (By.XPATH, "//button[@aria-label='Go to next page']")
        self.event_card_by_title = "//h4[contains(., '{title}')]"
        self.event_card_image = "(//div[@class='card-body']//img)[{num}]"
        self.event_card_title = "(//div[@class='card-body']//h4)[{num}]"
        self.event_card_description = "(//div[@class='card-body']//p)[{num}]"
        self.event_card_footer = "(//div[@class='card-footer'])[{num}]"
        self.single_event_date = (By.XPATH, "//div[@class='date icon-text']")
        self.single_event_about_section = (By.XPATH, "//div[@class='about']")
        self.single_event_buy_tickets_button = (By.XPATH, "//div[@class='purchase purchase-bottom']/a")
        self.single_event_opening_times_section = (By.XPATH, "//div[@class='opening-times']/div")
        self.single_event_location_section = (By.XPATH, "//div[@class='location']//p[1]")
        self.single_event_get_directions_link = (By.XPATH, "//div[@class='location']//p[2]/a")
        self.single_event_add_to_calendar_link = (By.XPATH, "//button[contains(@class, 'add-to-calendar')]")
        self.single_event_image_section = (By.XPATH, "//div[@class='slide-container']")

    def is_events_page_title_visible(self, title):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, self.page_title_by_title.format(title=title))))
        return page_title.is_displayed()

    def get_individual_event_title_text(self):
        return self.driver.find_element(*self.individual_event_title).text

    def is_heading_description_visible(self):
        heading = self.driver.find_elements(*self.heading_description)
        return True if len(heading) != 0 else False

    def get_heading_title_text(self):
        return self.driver.find_element(*self.events_page_title).text

    def get_heading_description_text(self):
        return self.driver.find_element(*self.heading_description).text

    def is_section_title_visible(self):
        heading = self.driver.find_elements(*self.section_title)
        return True if len(heading) != 0 else False

    def is_section_description_visible(self):
        heading = self.driver.find_elements(*self.section_description)
        return True if len(heading) != 0 else False

    def get_section_title_text(self):
        return self.driver.find_element(*self.section_title).text

    def get_section_description_text(self):
        return self.driver.find_element(*self.section_description).text

    def wait_individual_event_page_to_load(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located(self.back_button))

    def is_back_button_visible(self):
        return self.driver.find_element(*self.back_button).is_displayed()

    def click_back_button(self):
        self.driver.find_element(*self.back_button).click()

    def get_event_cards_number(self):
        return len(self.driver.find_elements(*self.event_card))

    def is_event_card_visible(self, num):
        cards = self.driver.find_elements(*self.event_card)
        return cards[num].is_displayed()

    def is_event_card_visible_by_title(self, title):
        card = self.driver.find_elements(By.XPATH, self.event_card_by_title.format(title=title))
        return True if len(card) != 0 else False

    def click_event_card_by_title(self, title):
        element = self.driver.find_element(By.XPATH, self.event_card_by_title.format(title=title) + "/../..")
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def is_event_card_image_visible(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_image.format(num=num)).is_displayed()

    def get_event_card_image(self, num):
        src = self.driver.find_element(By.XPATH, self.event_card_image.format(num=num)).get_attribute("src")
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', src)
        if filename:
            filename = filename.group(0)
        return filename.replace("%20", " ")

    def is_event_card_title_visible(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_title.format(num=num)).is_displayed()

    def get_event_card_title_text(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_title.format(num=num)).text

    def is_event_card_description_visible(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_description.format(num=num)).is_displayed()

    def get_event_card_description_text(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_description.format(num=num)).text

    def is_event_card_date_visible(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_footer.format(num=num)).is_displayed()

    def get_event_card_date_text(self, num):
        return self.driver.find_element(By.XPATH, self.event_card_footer.format(num=num)).text

    def scroll_to_events_section(self):
        element = self.driver.find_element(*self.event_section)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

    def is_pagination_visible(self):
        element = self.driver.find_elements(*self.pagination)
        return True if len(element) != 0 else False

    def click_go_to_next_page_button(self):
        self.driver.find_element(*self.go_to_next_page).click()

    def scroll_to_pagination(self):
        element = self.driver.find_element(*self.pagination)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

    def is_single_event_date_visible(self):
        return self.driver.find_element(*self.single_event_date).is_displayed()

    def get_single_event_date_text(self):
        return self.driver.find_element(*self.single_event_date).text

    def is_single_event_about_section_visible(self):
        element = self.driver.find_elements(*self.single_event_about_section)
        return True if len(element) != 0 else False

    def get_single_event_about_section_text(self):
        text = ""
        section = self.driver.find_element(*self.single_event_about_section)
        paragraphs = section.find_elements(By.XPATH, ".//p")
        for paragraph in paragraphs:
            text = text + paragraph.text.strip()
        description_text = str(re.sub(' +', ' ', text))
        return description_text.strip()

    def is_buy_tickets_button_visible(self):
        element = self.driver.find_elements(*self.single_event_buy_tickets_button)
        return True if len(element) != 0 else False

    def click_buy_tickets_button(self):
        self.driver.find_element(*self.single_event_buy_tickets_button).click()

    def is_single_event_opening_times_section_visible(self):
        element = self.driver.find_elements(*self.single_event_opening_times_section)
        return True if len(element) != 0 else False

    def get_single_event_opening_times_section_text(self):
        opening_times_text = ""
        times = self.driver.find_element(*self.single_event_opening_times_section).text.split("\n")
        for single_time in times:
            opening_times_text = opening_times_text + single_time.strip()
        return opening_times_text

    def is_single_event_location_section_visible(self):
        element = self.driver.find_elements(*self.single_event_location_section)
        return True if len(element) != 0 else False

    def get_single_event_location_section_text(self):
        location_text = ""
        locations = self.driver.find_element(*self.single_event_location_section).text.split("\n")
        for location in locations:
            location_text = location_text + location.strip()
        return location_text

    def is_single_event_get_directions_link_visible(self):
        return self.driver.find_element(*self.single_event_get_directions_link).is_displayed()

    def click_single_event_get_directions_link(self, browser):
        element = self.driver.find_element(*self.single_event_get_directions_link)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()
        if browser == "firefox" or browser == "safari":
            time.sleep(3)

    def is_single_event_add_to_calendar_link_visible(self):
        return self.driver.find_element(*self.single_event_add_to_calendar_link).is_displayed()

    def click_single_event_add_to_calendar_link(self):
        self.driver.find_element(*self.single_event_add_to_calendar_link).click()

    def is_single_event_image_section_visible(self):
        return self.driver.find_element(*self.single_event_image_section).is_displayed()

    def get_single_event_images(self):
        image_list = []
        image_section = self.driver.find_element(*self.single_event_image_section)
        images = image_section.find_elements(By.XPATH, ".//img")
        for image in images:
            src = image.get_attribute("src")
            filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', src)
            if filename:
                filename = filename.group(0)
            image_list.append(filename.replace("%20", " "))
        return image_list

    @staticmethod
    def get_formatted_time(start_iso, end_iso):
        start_dt = datetime.fromisoformat(start_iso.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end_iso.replace("Z", "+00:00"))
        if os.getenv('CI') == 'true':
            hosted_tz = pytz.timezone("Europe/London")
        else:
            hosted_tz = pytz.timezone("Europe/Sofia")
        ast_tz = pytz.timezone("Asia/Riyadh")
        start_local = start_dt.astimezone(hosted_tz)
        end_local = end_dt.astimezone(hosted_tz)
        start_ast = start_dt.astimezone(ast_tz)
        end_ast = end_dt.astimezone(ast_tz)
        local_format = "{:%-d %B, %-I:%M%p}".format
        ast_format = "{:%-d %B, %-I:%M%p}".format
        now_local = datetime.now(hosted_tz).date()
        if start_local.date() == now_local:
            start_local_str = f"Today, {start_local.strftime('%-I:%M%p').lower()}"
            start_ast_str = f"Today, {start_ast.strftime('%-I:%M%p').lower()}"
        else:
            start_local_str = local_format(start_local).replace("AM", "am").replace("PM", "pm")
            start_ast_str = ast_format(start_ast).replace("AM", "am").replace("PM", "pm")
        end_local_str = local_format(end_local).replace("AM", "am").replace("PM", "pm")
        end_ast_str = ast_format(end_ast).replace("AM", "am").replace("PM", "pm")
        result = f"{start_local_str} - {end_local_str} ({start_ast_str} - {end_ast_str} AST)"
        return result

    @staticmethod
    def get_last_three_chronological_ordered_events(event_list):
        def parse_date(date_str):
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        sorted_events = sorted(event_list.items(), key=lambda x: parse_date(x[1]['start']))
        valid_titles = []
        now = datetime.now(pytz.UTC)
        for event_id, event in sorted_events:
            start_dt = parse_date(event['start'])
            end_dt = parse_date(event['end'])
            if start_dt < now and end_dt < now:
                continue
            if start_dt >= end_dt:
                continue
            valid_titles.append(event['title'])
            if len(valid_titles) == 3:
                break
        return valid_titles

    @classmethod
    def get_events_with_conditions(cls, api_obj, event_ids):
        full_description_event = {}
        event_without_booking_link = {}
        for event_id in event_ids:
            temp_event = api_obj.get_individual_event(event_id)
            if not bool(event_without_booking_link) and not bool(temp_event["booking_link"]):
                event_without_booking_link = temp_event
            if (not bool(full_description_event) and bool(temp_event["booking_link"]) and
                    bool(temp_event["opening_times"]) and bool(temp_event["address"]) and
                    bool(temp_event["description"])):
                full_description_event = temp_event
            if bool(event_without_booking_link) and bool(full_description_event):
                break
        return event_without_booking_link, full_description_event
