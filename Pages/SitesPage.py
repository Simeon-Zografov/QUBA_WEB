import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def split_historic_and_retail_sites(site_list, site_type):
    filtered_sites = {}
    for site_id, site in site_list.items():
        if site["type"] == site_type:
            filtered_sites[site_id] = {"title": site["title"], "summary": site["summary"]}
    return filtered_sites


def get_site_number(site_list, site_type):
    filtered_sites = split_historic_and_retail_sites(site_list, site_type)
    return len(filtered_sites)


class Sites:

    def __init__(self, driver):
        self.driver = driver
        self.sites_page_title = (By.XPATH, "//h1[.='Experience yesterday, today']")
        self.historic_sites_button = (By.XPATH, "//button[@aria-controls='Historic']")
        self.retail_sites_button = (By.XPATH, "//button[@aria-controls='Retail']")
        self.historic_site_cards = (By.XPATH, "//div[@id='Historic']//div[@class='card app-carousel-card']")
        self.retail_site_cards = (By.XPATH, "//div[@id='Retail']//div[@class='card app-carousel-card']")
        self.next_pagination_button = (By.XPATH, "//button[@aria-label='Go to next page']")
        self.individual_site_title = (By.XPATH, "//h1")
        self.individual_site_summary = (By.XPATH, "//div[@class='summary']")
        self.individual_site_about = (By.XPATH, "//div[@class='about']/p")
        self.individual_site_location = (By.XPATH, "//div[@class='location']/p[not(a)]")
        self.individual_site_opening_times = (By.XPATH, "//div[@class='opening-times']/div")
        self.back_button = (By.XPATH, "//button[@class='btn btn-md btn-link app-button back-link icon-text']")
        self.exhibit_section = (By.XPATH, "//h2[.='Exhibits at this site']")
        self.exhibit_cards = (By.XPATH, "//div[@class='card app-carousel-card']")

    def is_sites_page_title_visible(self):
        wait = WebDriverWait(self.driver, 30)
        page_title = wait.until(EC.visibility_of_element_located(self.sites_page_title))
        return page_title.is_displayed()

    def click_historic_button(self):
        self.driver.find_element(*self.historic_sites_button).click()

    def click_retail_button(self):
        self.driver.find_element(*self.retail_sites_button).click()

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

    def is_pagination_visible(self, site_type):
        element_list = self.driver.find_elements(By.XPATH, f"//div[@id='{site_type}']//ul[@aria-label='Pagination']")
        if len(element_list) != 0:
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
        self.driver.execute_script(f"window.scrollTo({x}, {y - 100});")
        time.sleep(1)
        element.click()

    def click_next_pagination_button(self):
        self.driver.find_element(*self.next_pagination_button).click()

    def scroll_to_pagination(self):
        element = self.driver.find_element(*self.next_pagination_button)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 100});")
        time.sleep(1)

    def scroll_to_tab_buttons(self):
        element = self.driver.find_element(*self.historic_sites_button)
        location = element.location
        x = location['x']
        y = location['y']
        self.driver.execute_script(f"window.scrollTo({x}, {y - 100});")
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
        self.driver.find_element(*self.back_button).click()

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
