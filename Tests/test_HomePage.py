import json
import os
import random
import shutil
import subprocess
import time
import allure
import pytest
from selenium import webdriver
from pytest_check import check
from allure import severity, severity_level
from Common.APIRequests import APIRequests
from Pages.Admin import Admin
from Pages.EventsPage import Events
from Pages.HomePage import HomePage
from Pages.MainNavigation import MainNavigation
from Pages.SitesPage import Sites
from Common.BaseClass import BaseClass
from selenium.webdriver.chrome.service import Service as ChromeService


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestHomePage(BaseClass):
    current_browser = None
    home_page_content = {'hero_title': 'Bringing the past into the future',
                         'hero_subtitle': 'A visual journey through the history of Al Madinah Cras mattis consectetur purus sit amet fermentum. Sed posuere consectetur est at lobortis.',
                         'hero_image': 'hero-2-bg.jpg', 'hero_link_text': 'Explore now', 'hero_link_url': '/sites',
                         'download_title': 'History in the palm of your hand',
                         'download_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce blandit sollicitudin nunc.Aenean metus magna, faucibus eget tellus nec, molestie bibendum dui. Nunc pretium, est eget varius sodales, lectus lorem fermentum tellus, at tincidunt risus nulla ut lacus.',
                         'download_image': 'app-screen.png',
                         'download_stats': {'13,500,000': 'Annual visitors', '200': 'Points of interest',
                                            '50': 'Guided tours'}, 'site_carousel_title': 'Plan your visit to Madinah',
                         'site_carousel_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce blandit sollicitudin nunc. ',
                         'site_carousel_link_text': 'View all', 'site_carousel_link_url': '/sites',
                         'site_carousel_sites': {0: 'Sowalla Date Farm', 1: 'Quba Mosque', 2: 'Atban Bin Malik Mosque'},
                         'event_carousel_title': 'Events in Madinah',
                         'event_carousel_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce blandit sollicitudin nunc. ',
                         'event_carousel_link_text': 'View all', 'event_carousel_link_url': '/events'}

    # home_page_content = {}

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestHomePage.current_browser = request.node.callspec.params["driver"]

    # @pytest.fixture(scope="class", autouse=True)
    # def get_home_page_content(self, driver):
    #     admin_obj = Admin(driver)
    #     admin_obj.switch_to_admin()
    #     TestHomePage.home_page_content = admin_obj.get_home_page_content()
    #     print(TestHomePage.home_page_content)
    #     admin_obj.close_admin()

    @classmethod
    def setup_class(cls):
        cls.api_requests = APIRequests()
        cls.site_list = cls.api_requests.get_sites_list()
        cls.event_list = cls.api_requests.get_events_list()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("User is navigated to the Home page")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58319", "C58319")
    def test_1(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(BaseClass.url)
        with check, allure.step("Check the page title"):
            assert home_page_obj.is_home_page_title_visible(TestHomePage.home_page_content["hero_title"])
        with check, allure.step("Logo is visible"):
            assert main_nav_obj.is_app_logo_visible()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check sections appearance")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58320", "C58320")
    def test_2(self, driver):
        home_page_obj = HomePage(driver)
        nav_bar_obj = MainNavigation(driver)
        with check, allure.step("Check is navigation bar visible"):
            assert nav_bar_obj.is_nav_bar_visible()
        with check, allure.step("Check is Hero banner visible"):
            assert home_page_obj.is_hero_banner_visible()
        with check, allure.step("Check is App Download section visible"):
            assert home_page_obj.is_hero_banner_visible()
        with check, allure.step("Check is Sites carousel visible"):
            assert home_page_obj.is_site_carousel_section_visible()
        with check, allure.step("Check is Events carousel visible"):
            assert home_page_obj.is_event_carousel_section_visible()
        with check, allure.step("Check is Footer visible"):
            assert home_page_obj.is_app_footer_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner appearance")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58334", "C58334")
    def test_3(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58334: Check is Hero banner title visible"):
            assert home_page_obj.is_hero_banner_title_visible()
        with check, allure.step("C58334: Check is Hero banner subtitle visible"):
            assert home_page_obj.is_hero_banner_subtitle_visible()
        with check, allure.step("C58334: Check is Hero banner button visible"):
            assert home_page_obj.is_hero_banner_button_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner image")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58335", "C58335")
    def test_4(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58335: Check Hero banner image"):
            assert home_page_obj.get_hero_banner_image() == TestHomePage.home_page_content["hero_image"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner title")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58336", "C58336")
    def test_5(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58336: Check Hero banner title text"):
            assert home_page_obj.get_hero_banner_title_text() == TestHomePage.home_page_content["hero_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner subtitle")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58337", "C58337")
    def test_6(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58337: Check Hero banner subtitle text"):
            assert home_page_obj.get_hero_banner_subtitle_text() == TestHomePage.home_page_content["hero_subtitle"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner button")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58338", "C58338")
    def test_7(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        with check, allure.step("C58338: Check Hero banner button text"):
            assert home_page_obj.get_hero_banner_button_text().strip() == TestHomePage.home_page_content[
                "hero_link_text"].strip()
        with check, allure.step("C58338: Click Hero banner button"):
            home_page_obj.click_hero_banner_button()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == BaseClass.url[:-1] + TestHomePage.home_page_content["hero_link_url"]
        main_nav_obj.click_home_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check Download section appearance")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58339", "C58339")
    def test_8(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58339: Check is section title visible"):
            assert home_page_obj.is_download_title_visible()
        with check, allure.step("C58339: Check is section description visible"):
            assert home_page_obj.is_download_description_visible()
        with check, allure.step("C58339: Check is section image visible"):
            assert home_page_obj.is_download_image_visible()
        with check, allure.step("C58339: Check is section statistics visible"):
            assert home_page_obj.is_download_stats_section_visible()
        with check, allure.step("C58339: Check is section google play button visible"):
            assert home_page_obj.is_download_google_play_button_visible()
        with check, allure.step("C58339: Check is section app store button visible"):
            assert home_page_obj.is_download_app_store_button_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section image")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58340", "C58340")
    def test_9(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58340: Check section image"):
            assert home_page_obj.get_download_image() == TestHomePage.home_page_content["download_image"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section title")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58341", "C58341")
    def test_10(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58341: Check section title"):
            assert home_page_obj.get_download_title_text() == TestHomePage.home_page_content["download_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section description")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58342", "C58342")
    def test_11(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58342: Check section description"):
            assert home_page_obj.get_download_description_text() == TestHomePage.home_page_content[
                "download_description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section analytic pairs")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58343", "C58343")
    def test_12(self, driver):
        home_page_obj = HomePage(driver)
        stat_keys = list(TestHomePage.home_page_content["download_stats"].keys())
        stat_values = list(TestHomePage.home_page_content["download_stats"].values())
        with check, allure.step("C58343: Check the number of pairs"):
            expected_number = len(stat_keys)
            actual_number = home_page_obj.get_stats_pairs_number()
            assert expected_number == actual_number
        for i in range(home_page_obj.get_stats_pairs_number()):
            with check, allure.step(f"C58343: {stat_values[i]} and {stat_keys[i]} pair is correct"):
                actual_value, actual_description = home_page_obj.get_download_stats(i)
                assert actual_value == stat_keys[i] and actual_description == stat_values[i]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Click Download section Google Play button")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58345", "C58345")
    def test_13(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58345: Check the redirected url"):
            assert "play.google.com" in home_page_obj.get_download_google_play_button_url()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Click Download section App Store button")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58344", "C58344")
    def test_14(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58344: Check the redirected url"):
            assert "apps.apple.com" in home_page_obj.get_download_app_store_button_url()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check sites carousel appearance")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58378", "C58378")
    def test_15(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58378: Check is site carousel title visible"):
            assert home_page_obj.is_site_carousel_title_visible()
        with check, allure.step("C58378: Check is site carousel description visible"):
            assert home_page_obj.is_site_carousel_description_visible()
        with check, allure.step("C58378: Check is site carousel button visible"):
            assert home_page_obj.is_site_carousel_button_visible()
        with check, allure.step("C58378: Check are site carousel site cards visible"):
            assert home_page_obj.is_site_carousel_cards_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check site carousel title")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58392", "C58392")
    def test_16(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58392: Check site carousel title"):
            assert home_page_obj.get_site_carousel_title_text() == TestHomePage.home_page_content["site_carousel_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check site carousel description")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58393", "C58393")
    def test_17(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58393: Check site carousel description"):
            assert home_page_obj.get_site_carousel_description_text().strip() == TestHomePage.home_page_content[
                "site_carousel_description"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check presented sites in the sites carousel")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58394", "C58394")
    def test_18(self, driver):
        home_page_obj = HomePage(driver)
        site_list = self.site_list
        cms_sites = TestHomePage.home_page_content["site_carousel_sites"]
        with check, allure.step("C58394: Check site cards number"):
            assert home_page_obj.get_site_carousel_cards_number() == len(cms_sites.keys())
        i = 0
        for cms_site in cms_sites.values():
            expected_image = ""
            expected_description = ""
            for site_id, site in site_list.items():
                if cms_site == site["title"]:
                    expected_description = site["summary"]
                    expected_image = site["image"]
                    break
            with check, allure.step(f"C58394: Check {cms_site} title"):
                assert home_page_obj.get_site_carousel_card_title(i).strip() == cms_site.strip()
            with check, allure.step(f"C58394: Check {cms_site} description"):
                assert home_page_obj.get_site_carousel_card_description(i).strip() == expected_description.strip()
            with check, allure.step(f"C58394: Check {cms_site} image"):
                assert home_page_obj.get_site_carousel_card_image(i).strip() == expected_image.strip()
            i = i + 1

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check presented sites order")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58397", "C58397")
    def test_19(self, driver):
        home_page_obj = HomePage(driver)
        cms_sites = TestHomePage.home_page_content["site_carousel_sites"]
        correct_order = True
        for i in range(len(cms_sites.values())):
            if cms_sites[i].strip() != home_page_obj.get_site_carousel_card_title(i).strip():
                correct_order = False
        with check, allure.step("C58397: Check site cards order"):
            assert correct_order

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check site carousel button")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58395", "C58395")
    def test_20(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        with check, allure.step("C58397: Check site carousel button text"):
            assert home_page_obj.get_site_carousel_button_text().strip() == TestHomePage.home_page_content[
                "site_carousel_link_text"].strip()
        with check, allure.step("C58338: Click Hero banner button"):
            home_page_obj.click_site_carousel_button()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == BaseClass.url[:-1] + TestHomePage.home_page_content["site_carousel_link_url"]
        main_nav_obj.click_home_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Click on site carousel card")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58608", "C58608")
    def test_21(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        sites_obj = Sites(driver)
        sites_number = len(TestHomePage.home_page_content["site_carousel_sites"].values())
        random_site = random.randrange(sites_number)
        site_title = TestHomePage.home_page_content["site_carousel_sites"][random_site]
        with check, allure.step(f"User is navigated to {site_title} page"):
            home_page_obj.click_site_carousel_card(random_site)
            sites_obj.wait_individual_site_page_to_load()
            main_nav_obj.wait_page_to_load()
            assert sites_obj.get_individual_site_title_text() == site_title
        main_nav_obj.click_home_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check events carousel appearance")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58400", "C58400")
    @pytest.mark.dependency(name="test_22")
    def test_22(self, driver):
        home_page_obj = HomePage(driver)
        events_list = self.event_list
        if len(list(events_list.keys())) == 0:
            pytest.skip("No events available")
        with check, allure.step("C58400: Check is event carousel title visible"):
            assert home_page_obj.is_event_carousel_title_visible()
        with check, allure.step("C58400: Check is event carousel description visible"):
            assert home_page_obj.is_event_carousel_description_visible()
        with check, allure.step("C58400: Check is event carousel button visible"):
            assert home_page_obj.is_event_carousel_button_visible()
        with check, allure.step("C58400: Check are event carousel event cards visible"):
            assert home_page_obj.is_event_carousel_cards_visible()
        cond = random.choice([True, False])
        assert cond

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check event carousel title")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58401", "C58401")
    @pytest.mark.dependency(depends=["test_22"])
    def test_23(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58401: Check event carousel title"):
            assert home_page_obj.get_event_carousel_title_text() == TestHomePage.home_page_content[
                "event_carousel_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check event carousel description")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58402", "C58402")
    @pytest.mark.dependency(depends=["test_22"])
    def test_24(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58402: Check event carousel description"):
            assert home_page_obj.get_event_carousel_description_text().strip() == TestHomePage.home_page_content[
                "event_carousel_description"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check presented events in the events carousel")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58403", "C58403")
    @pytest.mark.dependency(depends=["test_22"])
    def test_25(self, driver):
        home_page_obj = HomePage(driver)
        events_list = self.event_list
        events_number = len(events_list.keys())
        with check, allure.step("C58403: Check event cards number"):
            if events_number > 3:
                expected_number = 3
            else:
                expected_number = events_number
            assert home_page_obj.get_event_carousel_cards_number() == expected_number
        i = 0
        for event_id, event in events_list.items():
            if i >= 3:
                break
            expected_title = event["title"]
            expected_summary = event["summary"]
            expected_image = event["image"]
            expected_time = home_page_obj.get_formatted_time(event["start"], event["end"])
            with check, allure.step(f"C58394: Check {expected_title} title"):
                assert home_page_obj.get_event_carousel_card_title(i).strip() == expected_title.strip()
            with check, allure.step(f"C58394: Check {expected_title} description"):
                assert home_page_obj.get_event_carousel_card_description(i).strip() == expected_summary.strip()
            with check, allure.step(f"C58394: Check {expected_title} image"):
                assert home_page_obj.get_event_carousel_card_image(i).strip() == expected_image.strip()
            with check, allure.step(f"C58394: Check {expected_title} time"):
                assert home_page_obj.get_event_carousel_card_time(i).strip() == expected_time.strip()
            i = i + 1

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check presented events order")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58404", "C58404")
    @pytest.mark.dependency(depends=["test_22"])
    def test_26(self, driver):
        home_page_obj = HomePage(driver)
        events_list = self.event_list
        event_order = home_page_obj.get_last_three_chronological_ordered_events(events_list)
        i = 0
        for event_title in event_order:
            with check, allure.step(f"{event_title} in in the correct position"):
                assert home_page_obj.get_event_carousel_card_title(i).strip() == event_title.strip()
            i += 1

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check event carousel button")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58405", "C58405")
    @pytest.mark.dependency(depends=["test_22"])
    def test_27(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        with check, allure.step("C58405: Check event carousel button text"):
            assert home_page_obj.get_event_carousel_button_text().strip() == TestHomePage.home_page_content[
                "event_carousel_link_text"].strip()
        with check, allure.step("C58405: Click Hero banner button"):
            home_page_obj.click_event_carousel_button()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == BaseClass.url[:-1] + TestHomePage.home_page_content["event_carousel_link_url"]
        main_nav_obj.click_home_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Click on event carousel card")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58609", "C58609")
    @pytest.mark.dependency(depends=["test_22"])
    def test_28(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        events_obj = Events(driver)
        events_list = self.event_list
        event_ids = list(events_list.keys())
        event_number = len(event_ids)
        if event_number >= 3:
            event_number = 3
        random_event = random.randrange(event_number)
        event_title = events_list[event_ids[random_event]]["title"]
        with check, allure.step(f"User is navigated to {event_title} page"):
            home_page_obj.click_event_carousel_card(random_event)
            events_obj.wait_individual_event_page_to_load()
            main_nav_obj.wait_page_to_load()
            assert events_obj.get_individual_event_title_text() == event_title
        main_nav_obj.click_home_button()
        main_nav_obj.wait_page_to_load()

    # @severity(severity_level.NORMAL)
    # @allure.feature('Home page')
    # @allure.title("Event carousel cards without events")
    # @allure.issue("QP-269", "Story QP-269")
    # @allure.issue("QP-356", "Epic QP-356")
    # @allure.testcase("58609", "C58609")
    # @pytest.mark.dependency(depends=["test_22"])
    # def test_29(self):
    #     project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #     chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
    #     serv = ChromeService(chrome_driver_path)
    #     options = SeleniumWireOptions(
    #         disable_encoding=True
    #     )
    #
    #     wire_driver = webdriver.Chrome(service=serv, seleniumwire_options=options)
    #
    #     def response_interceptor(request, response):
    #         if 'https://cms-qaclm.raseel.city/graphql' in request.url:
    #             body = response.body.decode('utf-8')
    #             json_data = json.loads(body)
    #             print(json_data)
    #
    #             if 'data' in json_data and 'events' in json_data['data'] and 'data' in json_data['data']['events']:
    #                 json_data['data']['events']['data'] = []
    #
    #             modified_body = json.dumps(json_data)
    #             print(modified_body)
    #             response.body = modified_body.encode('utf-8')
    #
    #     wire_driver.response_interceptor = response_interceptor
    #     wire_driver.get(BaseClass.url)
    #     main_nav_obj = MainNavigation(wire_driver)
    #     home_page_obj = HomePage(wire_driver)
    #     main_nav_obj.wait_page_to_load()
    #     with check, allure.step("Events carousel is empty"):
    #         assert home_page_obj.get_event_carousel_cards_number() == 0
    #     wire_driver.quit()

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Event carousel cards without events")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58610", "C58610")
    # @pytest.mark.dependency(depends=["test_22"])
    @pytest.mark.parametrize("proxy_driver", ["home_page_test_29"], indirect=True)
    def test_29(self, proxy_driver):
        if TestHomePage.current_browser == "firefox" or TestHomePage.current_browser == "safari":
            pytest.skip(f"Mitmproxy is not supported on {TestHomePage.current_browser}")
        # request.param = TestHomePage.current_browser
        # proxy_driver = proxy_driver(TestHomePage.current_browser, "home_page_test_29")
        # browser = TestHomePage.current_browser
        # proxy_driver = BaseClass.proxy_driver(browser)
        proxy_driver.get(BaseClass.url)

        # Replace this with your test's page load and interaction logic
        main_nav_obj = MainNavigation(proxy_driver)
        home_page_obj = HomePage(proxy_driver)
        main_nav_obj.wait_page_to_load()

        # Example assertion to check if the events carousel is empty
        with check, allure.step("C58610: Events carousel is empty"):
            assert home_page_obj.get_event_carousel_cards_number() == 0
        # project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # browser = TestHomePage.current_browser
        # chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
        # mitmdump_path = shutil.which("mitmdump")
        # script_path = os.path.join(project_folder, "Common", "ResponseInterception.py")

        # if mitmdump_path is None:
        #     raise FileNotFoundError("mitmdump executable not found in PATH. Please ensure mitmproxy is installed.")

        # Start mitmdump with the response modification script
        # mitmdump_process = subprocess.Popen([mitmdump_path, "-s", script_path, "--listen-port", port,
        #                                      "--set", "test_name=home_page_test_29"])
        # try:
            # # Configure Chrome options to route through mitmproxy's default proxy
            # options = webdriver.ChromeOptions()
            # options.add_argument('--proxy-server=http://127.0.0.1:8082')  # mitmproxy default proxy
            # options.add_argument('--ignore-certificate-errors')  # Bypass cert errors if needed for testing
            #
            # # Initialize the WebDriver
            # serv = ChromeService(chrome_driver_path)
            # proxy_driver = webdriver.Chrome(service=serv, options=options)
            # browser = TestHomePage.current_browser
            # proxy_driver = BaseClass.proxy_driver(browser)
            # proxy_driver.get(BaseClass.url)
            #
            # # Replace this with your test's page load and interaction logic
            # main_nav_obj = MainNavigation(proxy_driver)
            # home_page_obj = HomePage(proxy_driver)
            # main_nav_obj.wait_page_to_load()
            #
            # # Example assertion to check if the events carousel is empty
            # with check, allure.step("C58610: Events carousel is empty"):
            #     assert home_page_obj.get_event_carousel_cards_number() == 0
        #
        # finally:
        #     # Clean up by closing the WebDriver and stopping mitmdump
        #     proxy_driver.quit()
        #     mitmdump_process.terminate()
        #     mitmdump_process.wait()

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check main navigation")
    def test_30(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        sites_obj = Sites(driver)
        with check, allure.step("User is navigated to Sites page"):
            main_nav_obj.click_sites_button()
            assert sites_obj.is_sites_page_title_visible()
        with check, allure.step("User is navigated to Home page"):
            main_nav_obj.click_home_button()
            assert home_page_obj.is_home_page_title_visible(TestHomePage.home_page_content["hero_title"])

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check language switch")
    def test_31(self, driver):
        main_nav_obj = MainNavigation(driver)
        with check, allure.step("English is selected by default"):
            assert main_nav_obj.get_page_language() == "en-US"
        with check, allure.step("Successful language change"):
            main_nav_obj.click_language_switch_button()
            main_nav_obj.click_language_button()
            if TestHomePage.current_browser == "safari":
                time.sleep(2)
            assert main_nav_obj.get_page_language() == "ar-SA"
