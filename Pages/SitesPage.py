import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def split_historic_and_retail_sites(site_list, site_type):
    filtered_sites = {}
    for site_id, site in site_list.items():
        if site["type"] == site_type:
            filtered_sites[site_id] = {"title": site["title"], "summary": site["summary"], "image": site["image"]}
    return filtered_sites


def get_site_number(site_list, site_type):
    filtered_sites = split_historic_and_retail_sites(site_list, site_type)
    return len(filtered_sites)


class Sites:

    def __init__(self, driver):
        self.driver = driver
        self.sites_page_title = (By.XPATH, "//h1")
        self.heading_description = (By.XPATH, "//div[@class='heading-top']//div")
        self.app_tabs_title = (By.XPATH, "//div[@class='app-tabs']//h2")
        self.app_tabs_description = (By.XPATH, "//div[@class='app-tabs']//div[@class='description']")
        self.tab_buttons_section = (By.XPATH, "//ul[@class='nav nav-tabs']")
        self.historic_sites_button = (By.XPATH, "//button[@aria-controls='Historic']")
        self.retail_sites_button = (By.XPATH, "//button[@aria-controls='Retail']")
        self.saved_sites_button = (By.XPATH, "//button[@aria-controls='savedSites']")
        self.historic_site_cards = (By.XPATH, "//div[@id='Historic']//div[@class='card app-carousel-card']")
        self.retail_site_cards = (By.XPATH, "//div[@id='Retail']//div[@class='card app-carousel-card']")
        self.saved_site_cards = (By.XPATH, "//div[@id='savedSites']//div[@class='card app-carousel-card']")
        self.next_pagination_button = (By.XPATH, "//button[@aria-label='Go to next page']")
        self.individual_site_title = (By.XPATH, "//h1")
        self.individual_site_summary = (By.XPATH, "//div[@class='summary']")
        self.individual_site_about = (By.XPATH, "//div[@class='about']/p")
        self.individual_site_location = (By.XPATH, "//div[@class='location']/p[not(a)]")
        self.individual_site_opening_times = (By.XPATH, "//div[@class='opening-times']/div")
        self.back_button = (By.XPATH, "//button[@class='btn btn-md btn-link app-button back-link icon-text']")
        self.exhibit_section = (By.XPATH, "//h2[.='Exhibits at this site']")
        self.exhibit_cards = (By.XPATH, "//div[@class='card app-carousel-card']")
        self.empty_tab_section = (By.XPATH, "//div[@class='empty-tabs']")
        self.single_site_header = (By.XPATH, "//header[@class='header']")
        self.single_site_image_section = (By.XPATH, "//div[contains(@class, 'image-slider')]")
        self.single_site_exhibit_section = (By.XPATH, "//div[@class='exhibits']")
        self.single_site_travel_section = (By.XPATH, "//section[@class='site-travel-info']")
        self.single_site_footer = (By.ID, "site-footer")
        self.single_site_summary = (By.XPATH, "//div[@class='summary']")
        self.single_site_about = (By.XPATH, "//div[@class='about']")
        self.single_site_opening_times = (By.XPATH, "//div[@class='opening-times']")
        self.single_site_location = (By.XPATH, "//div[@class='location']")
        self.single_site_amenities = (By.XPATH, "//div[@class='amenities']")
        self.single_site_get_directions_link = (By.XPATH, "//div[@class='location']//a")
        self.single_site_exhibit_cards = (By.XPATH, "//div[@class='card app-carousel-card']")
        self.single_site_exhibit_title = (By.XPATH, "//div[@class='card app-carousel-card']//h4")
        self.single_site_exhibit_summary = (By.XPATH, "//div[@class='card app-carousel-card']//p")
        self.single_site_exhibit_image = (By.XPATH, "//div[@class='card app-carousel-card']//img")
        self.save_site_button = (By.XPATH, "//button[@class='save-button']")
        self.save_site_icon = (By.XPATH, "//button[@class='save-button']//*[@class='app-icon save-icon']")

    def is_sites_page_title_visible(self, title):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located((By.XPATH, f"//h1[.='{title}']")))
        return page_title.is_displayed()

    def is_heading_description_visible(self):
        heading = self.driver.find_elements(*self.heading_description)
        return True if len(heading) != 0 else False

    def get_heading_title_text(self):
        return self.driver.find_element(*self.sites_page_title).text

    def get_heading_description_text(self):
        return self.driver.find_element(*self.heading_description).text

    def get_app_tabs_title_text(self):
        return self.driver.find_element(*self.app_tabs_title).text

    def get_app_tabs_description_text(self):
        return self.driver.find_element(*self.app_tabs_description).text.strip()

    def click_historic_button(self):
        self.driver.find_element(*self.historic_sites_button).click()

    def click_retail_button(self):
        self.driver.find_element(*self.retail_sites_button).click()

    def click_saved_sites_button(self):
        self.driver.find_element(*self.saved_sites_button).click()
        time.sleep(0.5)

    def is_saved_sites_button_visible(self):
        button = self.driver.find_elements(*self.saved_sites_button)
        if len(button) > 0:
            return True
        else:
            return False

    def click_site_tab_button(self, site_type):
        self.driver.find_element(By.XPATH, f"//button[@aria-controls='{site_type}']").click()

    def is_historic_tab_selected(self):
        attribute = self.driver.find_element(*self.historic_sites_button).get_attribute("aria-selected")
        if attribute == "true":
            return True
        else:
            return False

    def is_retail_tab_selected(self):
        attribute = self.driver.find_element(*self.retail_sites_button).get_attribute("aria-selected")
        if attribute == "true":
            return True
        else:
            return False

    def get_site_card_title(self, site_type, num):
        return self.driver.find_element(By.XPATH, f"(//div[@id='{site_type}']//div[@class='card-body']/h4)[{num}]").text

    def get_site_card_summary(self, site_type, num):
        return self.driver.find_element(By.XPATH, f"(//div[@id='{site_type}']//div[@class='card-body']/p)[{num}]").text

    def get_site_card_image(self, site_type, num):
        src = self.driver.find_element(By.XPATH,
                                       f"(//div[@id='{site_type}']//div[@class='card-body']//img)[{num}]").get_attribute(
            "src")
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', src)
        if filename:
            filename = filename.group(0)
        return filename.replace("%20", " ")

    def is_site_card_title_visible(self, site_type, num):
        return self.driver.find_element(By.XPATH,
                                        f"(//div[@id='{site_type}']//div[@class='card-body']/h4)[{num}]").is_displayed()

    def is_site_card_summary_visible(self, site_type, num):
        return self.driver.find_element(By.XPATH,
                                        f"(//div[@id='{site_type}']//div[@class='card-body']/p)[{num}]").is_displayed()

    def is_site_card_image_visible(self, site_type, num):
        return self.driver.find_element(By.XPATH,
                                        f"(//div[@id='{site_type}']//div[@class='card-body']//img)[{num}]").is_displayed()

    def is_pagination_visible(self, site_type):
        element_list = self.driver.find_elements(By.XPATH, f"//div[@id='{site_type}']//ul[@aria-label='Pagination']")
        if len(element_list) != 0:
            return True
        else:
            return False

    def is_saved_site_icon_visible(self, site_type, site_title):
        icon = self.driver.find_elements(By.XPATH,
                                         f"//div[@id='{site_type}']//h4[contains(., '{site_title}')]//*[@class='app-icon card-pre-title-icon']")
        if len(icon) != 0:
            return True
        else:
            return False

    def get_site_cards_number(self, site_type):
        element_list = self.driver.find_elements(By.XPATH, f"//div[@id='{site_type}']//div[@class='card-body']")
        return len(element_list)

    def click_site_card(self, site_type, num):
        num = num + 1
        element = self.driver.find_element(By.XPATH, f"(//div[@id='{site_type}']//div[@class='card-body']/..)[{num}]")
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def click_site_card_by_title(self, site_type, site_title):
        element = self.driver.find_element(By.XPATH, f"//div[@id='{site_type}']//h4[contains(., '{site_title}')]/../..")
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def is_site_card_visible_by_title(self, site_type, site_title):
        time.sleep(5)
        cards = self.driver.find_elements(By.XPATH, f"//div[@id='{site_type}']//h4[contains(., '{site_title}')]")
        return True if len(cards) != 0 else False

    def click_next_pagination_button(self):
        self.driver.find_element(*self.next_pagination_button).click()

    def scroll_to_pagination(self):
        element = self.driver.find_element(*self.next_pagination_button)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

    def scroll_to_tab_buttons(self):
        element = self.driver.find_element(*self.tab_buttons_section)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

    def get_individual_site_title_text(self):
        return self.driver.find_element(*self.individual_site_title).text

    def get_individual_site_summary_text(self):
        return self.driver.find_element(*self.individual_site_summary).text

    def get_individual_site_description_text(self):
        return self.driver.find_element(*self.individual_site_about).text

    def is_individual_site_description_visible(self):
        element_list = self.driver.find_elements(*self.individual_site_about)
        if len(element_list) == 0:
            return False
        else:
            return True

    def get_individual_site_address_text(self):
        return self.driver.find_element(*self.individual_site_location).text

    def is_individual_site_address_visible(self):
        element_list = self.driver.find_elements(*self.individual_site_location)
        if len(element_list) == 0:
            return False
        else:
            return True

    def get_individual_site_opening_hours_text(self):
        return self.driver.find_element(*self.individual_site_opening_times).text

    def is_individual_site_opening_hours_visible(self):
        element_list = self.driver.find_elements(*self.individual_site_opening_times)
        if len(element_list) == 0:
            return False
        else:
            return True

    def click_back_button(self):
        element = self.driver.find_element(*self.back_button)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()

    def is_back_button_visible(self):
        return self.driver.find_element(*self.back_button).is_displayed()

    def wait_individual_site_page_to_load(self):
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located(self.back_button))

    def get_exhibit_card_title(self, num):
        return self.driver.find_element(By.XPATH, f"(//div[@class='card app-carousel-card']//h4)[{num}]").text

    def get_exhibit_card_summary(self, num):
        return self.driver.find_element(By.XPATH, f"(//div[@class='card app-carousel-card']//p)[{num}]").text

    def is_exhibit_section_visible(self):
        element_list = self.driver.find_elements(*self.exhibit_section)
        if len(element_list) != 0:
            return True
        else:
            return False

    def get_exhibit_cards_number(self):
        element_list = self.driver.find_elements(*self.exhibit_cards)
        return len(element_list)

    def is_empty_tab_section_visible(self):
        return self.driver.find_element(*self.empty_tab_section).is_displayed()

    def are_saved_sites_cards_visible(self):
        cards = self.driver.find_elements(*self.saved_site_cards)
        if len(cards) != 0:
            return True
        else:
            return False

    def get_saved_sites_cards_number(self):
        cards = self.driver.find_elements(*self.saved_site_cards)
        return len(cards)

    def is_single_site_header_visible(self):
        return self.driver.find_element(*self.single_site_header).is_displayed()

    def is_single_site_image_section_visible(self):
        return self.driver.find_element(*self.single_site_image_section).is_displayed()

    def scroll_to_single_site_image_section(self):
        element = self.driver.find_element(*self.single_site_image_section)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

    def is_single_site_exhibit_section_visible(self):
        section = self.driver.find_elements(*self.single_site_exhibit_section)
        if len(section) != 0:
            return True
        else:
            return False

    def is_single_site_travel_section_visible(self):
        element = self.driver.find_element(*self.single_site_travel_section)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        return element.is_displayed()

    def is_single_site_footer_visible(self):
        return self.driver.find_element(*self.single_site_footer).is_displayed()

    @classmethod
    def get_sites_with_conditions(cls, api_obj, sites_ids):
        one_image_site = {}
        several_images_site = {}
        full_description_site = {}
        site_with_exhibits = {}
        site_without_exhibits = {}
        for site_id in sites_ids:
            temp_site = api_obj.get_individual_site(site_id)
            if not bool(several_images_site) and len(temp_site[site_id]["images"]) >= 4:
                several_images_site = temp_site
            if not bool(one_image_site) and len(temp_site[site_id]["images"]) == 1:
                one_image_site = temp_site
            if not bool(site_with_exhibits) and len(temp_site[site_id]["exhibit"]) != 0:
                site_with_exhibits = temp_site
            if not bool(site_without_exhibits) and len(temp_site[site_id]["exhibit"]) == 0:
                site_without_exhibits = temp_site
            if (not bool(full_description_site) and len(temp_site[site_id]["facilities"]) != 0 and
                    bool(temp_site[site_id]["opening_hours"]) and bool(temp_site[site_id]["address"])):
                full_description_site = temp_site
            if (bool(several_images_site) and bool(one_image_site) and bool(site_with_exhibits) and
                    bool(site_without_exhibits) and bool(full_description_site)):
                break
        return one_image_site, several_images_site, full_description_site, site_with_exhibits, site_without_exhibits

    def is_single_site_summary_visible(self):
        return self.driver.find_element(*self.single_site_summary).is_displayed()

    def get_single_site_summary_text(self):
        return self.driver.find_element(*self.single_site_summary).text

    def is_single_site_about_visible(self):
        return self.driver.find_element(*self.single_site_about).is_displayed()

    def get_single_site_about_text(self):
        text = ""
        element = self.driver.find_element(*self.single_site_about)
        paragraphs = element.find_elements(By.XPATH, ".//p")
        for paragraph in paragraphs:
            text = text + paragraph.text.strip()
        description_text = str(re.sub(' +', ' ', text))
        return description_text.strip()

    def is_single_site_opening_times_visible(self):
        return self.driver.find_element(*self.single_site_opening_times).is_displayed()

    def get_single_site_opening_times_text(self):
        section = self.driver.find_element(*self.single_site_opening_times)
        return section.find_element(By.XPATH, ".//div").text.replace("<br>", "")

    def is_single_site_location_visible(self):
        return self.driver.find_element(*self.single_site_location).is_displayed()

    def get_single_site_location_text(self):
        section = self.driver.find_element(*self.single_site_location)
        return section.find_element(By.XPATH, ".//p[1]").text.replace("<br>", "")

    def is_single_site_amenities_visible(self):
        return self.driver.find_element(*self.single_site_amenities).is_displayed()

    def get_single_site_amenities_list(self):
        amenities_list = []
        amenities_section = self.driver.find_element(*self.single_site_amenities)
        amenities = amenities_section.find_elements(By.XPATH, ".//div[contains(@class, 'site-facility')]")
        for amenity in amenities:
            amenities_list.append(amenity.text.strip())
        return amenities_list

    def is_single_site_get_directions_link_visible(self):
        return self.driver.find_element(*self.single_site_get_directions_link).is_displayed()

    def click_single_site_get_directions_link(self, browser):
        element = self.driver.find_element(*self.single_site_get_directions_link)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)
        element.click()
        if browser == "firefox" or browser == "safari":
            time.sleep(3)

    def get_single_site_exhibit_cards_number(self):
        cards = self.driver.find_elements(*self.single_site_exhibit_cards)
        return len(cards)

    def get_single_site_exhibit_title(self, num):
        titles = self.driver.find_elements(*self.single_site_exhibit_title)
        return titles[num].text.strip()

    def get_single_site_exhibit_summary(self, num):
        summaries = self.driver.find_elements(*self.single_site_exhibit_summary)
        return summaries[num].text.strip()

    def get_single_site_exhibit_image(self, num):
        images = self.driver.find_elements(*self.single_site_exhibit_image)
        src = images[num].get_attribute("src")
        filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', src)
        if filename:
            filename = filename.group(0)
        return filename.replace("%20", " ")

    def scroll_to_exhibit_section(self):
        element = self.driver.find_element(*self.single_site_exhibit_section)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)

    def is_single_site_exhibit_card_clickable(self, num):
        cards = self.driver.find_elements(*self.single_site_exhibit_cards)
        link = cards[num].find_elements(By.XPATH, ".//a")
        if len(link) != 0:
            return True
        else:
            return False

    def is_save_site_button_visible(self):
        button = self.driver.find_elements(*self.save_site_icon)
        if len(button) != 0:
            return True
        else:
            return False

    def click_save_site_button(self):
        self.driver.find_element(*self.save_site_button).click()
        time.sleep(1)

    def is_save_site_icon_filled(self):
        fill = self.driver.find_element(*self.save_site_icon).get_attribute("fill")
        return True if fill == "currentColor" else False
