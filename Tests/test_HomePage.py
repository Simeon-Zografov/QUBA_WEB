import random
import time
import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.EventsPage import Events
from Pages.HomePage import HomePage
from Pages.MainNavigation import MainNavigation
from Pages.SitesPage import Sites
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestHomePage(BaseClass):
    current_browser = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        self.current_browser = request.node.callspec.params["driver"]

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("User is navigated to the Home page")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58319", "C58319")
    def test_1(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(self.url)
        with check, allure.step("Check the page title"):
            assert home_page_obj.is_home_page_title_visible(self.home_page_content["hero_title"])
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
            assert home_page_obj.get_hero_banner_image() == self.home_page_content["hero_image"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner title")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58336", "C58336")
    def test_5(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58336: Check Hero banner title text"):
            assert home_page_obj.get_hero_banner_title_text() == self.home_page_content["hero_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Hero Banner subtitle")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58337", "C58337")
    def test_6(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58337: Check Hero banner subtitle text"):
            assert home_page_obj.get_hero_banner_subtitle_text() == self.home_page_content["hero_subtitle"]

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
            assert home_page_obj.get_hero_banner_button_text().strip() == self.home_page_content[
                "hero_link_text"].strip()
        with check, allure.step("C58338: Click Hero banner button"):
            home_page_obj.click_hero_banner_button()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == self.url[:-1] + self.home_page_content["hero_link_url"]
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
            assert home_page_obj.get_download_image() == self.home_page_content["download_image"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section title")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58341", "C58341")
    def test_10(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58341: Check section title"):
            assert home_page_obj.get_download_title_text() == self.home_page_content["download_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section description")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58342", "C58342")
    def test_11(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58342: Check section description"):
            assert home_page_obj.get_download_description_text() == self.home_page_content[
                "download_description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check Download section analytic pairs")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58343", "C58343")
    def test_12(self, driver):
        home_page_obj = HomePage(driver)
        stat_keys = list(self.home_page_content["download_stats"].keys())
        stat_values = list(self.home_page_content["download_stats"].values())
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
            assert home_page_obj.get_site_carousel_title_text() == self.home_page_content["site_carousel_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Check site carousel description")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58393", "C58393")
    def test_17(self, driver):
        home_page_obj = HomePage(driver)
        with check, allure.step("C58393: Check site carousel description"):
            assert home_page_obj.get_site_carousel_description_text().strip() == self.home_page_content[
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
        cms_sites = self.home_page_content["site_carousel_sites"]
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
        cms_sites = self.home_page_content["site_carousel_sites"]
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
            assert home_page_obj.get_site_carousel_button_text().strip() == self.home_page_content[
                "site_carousel_link_text"].strip()
        with check, allure.step("C58338: Click Hero banner button"):
            home_page_obj.click_site_carousel_button()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == self.url[:-1] + self.home_page_content["site_carousel_link_url"]
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
        sites_number = len(self.home_page_content["site_carousel_sites"].values())
        random_site = random.randrange(sites_number)
        site_title = self.home_page_content["site_carousel_sites"][random_site]
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
            assert home_page_obj.get_event_carousel_title_text() == self.home_page_content[
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
            assert home_page_obj.get_event_carousel_description_text().strip() == self.home_page_content[
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
            assert home_page_obj.get_event_carousel_button_text().strip() == self.home_page_content[
                "event_carousel_link_text"].strip()
        with check, allure.step("C58405: Click Hero banner button"):
            home_page_obj.click_event_carousel_button()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == self.url[:-1] + self.home_page_content["event_carousel_link_url"]
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

    @severity(severity_level.NORMAL)
    @allure.feature('Home page')
    @allure.title("Event carousel cards without events")
    @allure.issue("QP-269", "Story QP-269")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58610", "C58610")
    @pytest.mark.parametrize("proxy_driver", ["home_page_test_29"], indirect=True)
    def test_29(self, proxy_driver):
        proxy_driver.get(self.url)
        main_nav_obj = MainNavigation(proxy_driver)
        home_page_obj = HomePage(proxy_driver)
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58610: Events carousel is empty"):
            assert home_page_obj.get_event_carousel_cards_number() == 0

    @severity(severity_level.CRITICAL)
    @allure.feature('Home page')
    @allure.title("Check main navigation")
    def test_30(self, driver):
        home_page_obj = HomePage(driver)
        main_nav_obj = MainNavigation(driver)
        sites_obj = Sites(driver)
        with check, allure.step("User is navigated to Sites page"):
            main_nav_obj.click_sites_button()
            assert sites_obj.is_sites_page_title_visible(self.sites_page_content["heading_title"])
        with check, allure.step("User is navigated to Home page"):
            main_nav_obj.click_home_button()
            assert home_page_obj.is_home_page_title_visible(self.home_page_content["hero_title"])

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
            if self.current_browser == "safari":
                time.sleep(2)
            assert main_nav_obj.get_page_language() == "ar-SA"
