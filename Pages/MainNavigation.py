import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainNavigation:

    def __init__(self, driver):
        self.driver = driver
        self.nav_bar = (By.XPATH, "//div[contains(@class, 'header-container')]")
        self.app_logo = (By.XPATH, "//a[contains(@class,'logo-link')]")
        self.home_button = (By.XPATH, "//a[.='Home']")
        self.sites_button = (By.XPATH, "//a[.='Sites']")
        self.about_button = (By.XPATH, "//a[.='About']")
        self.sponsors_button = (By.XPATH, "//a[.='Sponsors']")
        self.login_button = (By.XPATH, "//a[.='Log in']")
        self.logout_button = (By.XPATH, "//button[.='Log out']")
        self.language_switch_button = (By.ID, "lang-switcher")
        self.language_button = (By.XPATH, "//button[@role='menuitem']")

    def is_app_logo_visible(self):
        return self.driver.find_element(*self.app_logo).is_displayed()

    def is_nav_bar_visible(self):
        return self.driver.find_element(*self.nav_bar).is_displayed()

    def click_app_logo(self):
        self.driver.find_element(*self.app_logo).click()

    def click_home_button(self):
        self.driver.find_element(*self.home_button).click()

    def click_sites_button(self):
        self.driver.find_element(*self.sites_button).click()

    def click_about_button(self):
        self.driver.find_element(*self.about_button).click()

    def click_sponsors_button(self):
        self.driver.find_element(*self.sponsors_button).click()

    def click_login_button(self):
        self.driver.find_element(*self.login_button).click()

    def is_logout_button_visible(self, browser):
        if browser == "safari":
            time.sleep(5)
        wait = WebDriverWait(self.driver, 30)
        button = wait.until(EC.visibility_of_element_located(self.logout_button))
        return button.is_displayed()

    def click_logout_button(self):
        self.driver.find_element(*self.logout_button).click()

    def click_language_switch_button(self):
        self.driver.find_element(*self.language_switch_button).click()

    def click_language_button(self):
        self.driver.find_element(*self.language_button).click()

    def get_page_language(self):
        return self.driver.find_element(By.XPATH, "//html").get_attribute("lang")

    def wait_page_to_load(self):
        time.sleep(2)
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h1")))
