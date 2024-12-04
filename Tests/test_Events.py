import os
import time
from datetime import datetime
import allure
import pytest
import random
import pytz
from pytest_check import check
from allure import severity, severity_level
from Pages.EventsPage import Events
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestEvents(BaseClass):
    full_description_event = {}
    event_without_booking_link = {}

    @severity(severity_level.CRITICAL)
    @allure.feature('Events')
    @allure.title("User is navigated to the Events page")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58447", "C58447")
    @pytest.mark.dependency(name="test_1")
    def test_1(self, driver):
        events_obj = Events(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(self.url)
        main_nav_obj.wait_page_to_load()
        main_nav_obj.click_events_button()
        with check, allure.step("C58447: Events page is loaded"):
            assert events_obj.is_events_page_title_visible(self.events_page_content["heading_title"])

    @severity(severity_level.NORMAL)
    @allure.feature('Events')
    @allure.title("Events pages section titles")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58454", "C58454")
    @pytest.mark.dependency(depends=["test_1"])
    def test_2(self, driver):
        events_obj = Events(driver)
        with check, allure.step("C58454: Events page title is visible"):
            assert events_obj.is_events_page_title_visible(self.events_page_content["heading_title"])
        with check, allure.step("C58454: Section title is visible"):
            assert events_obj.is_section_title_visible()
        with check, allure.step("C58454: Events page title text is correct"):
            assert events_obj.get_heading_title_text().strip() == self.events_page_content["heading_title"].strip()
        with check, allure.step("C58454: Section title text is correct"):
            assert events_obj.get_section_title_text().strip() == self.events_page_content["section_title"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('Events')
    @allure.title("Events pages section description")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58455", "C58455")
    @pytest.mark.dependency(depends=["test_1"])
    def test_3(self, driver):
        events_obj = Events(driver)
        with check, allure.step("C58455: Events page description is visible"):
            assert events_obj.is_heading_description_visible()
        with check, allure.step("C58455: Section description is visible"):
            assert events_obj.is_section_description_visible()
        with check, allure.step("C58455: Events page description text is correct"):
            assert events_obj.get_heading_description_text() == self.events_page_content["heading_description"]
        with check, allure.step("C58455: Section description text is correct"):
            assert events_obj.get_section_description_text() == self.events_page_content["section_description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Events')
    @allure.title("Events section appearance")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58456", "C58456")
    @allure.testcase("58468", "C58468")
    @allure.testcase("58457", "C58457")
    @allure.testcase("58458", "C58458")
    @pytest.mark.dependency(depends=["test_1"])
    def test_4(self, driver):
        events_obj = Events(driver)
        events_obj.scroll_to_events_section()
        expected_card_number = len(list(self.event_list.keys()))
        if expected_card_number > 9:
            with check, allure.step("C58456: Nine cards are visible on the page"):
                assert events_obj.get_event_cards_number() == 9
            with check, allure.step("C58468: Pagination is visible"):
                assert events_obj.is_pagination_visible()
        else:
            with check, allure.step("C58456: The number of cards are visible on the page is correct"):
                assert events_obj.get_event_cards_number() == expected_card_number
            with check, allure.step("C58468: Pagination is not visible"):
                assert not events_obj.is_pagination_visible()
        num = 1
        for event_id, event in self.event_list.items():
            with check, allure.step(f"C58456: {event['title']} is displayed"):
                assert events_obj.is_event_card_visible_by_title(event['title'])
            with check, allure.step(f"C58457: {event['title']} title is visible"):
                assert events_obj.is_event_card_title_visible(num)
            with check, allure.step(f"C58458: {event['title']} title is correct"):
                assert events_obj.get_event_card_title_text(num).strip() == event["title"].strip()
            with check, allure.step(f"C58457: {event['title']} description is visible"):
                assert events_obj.is_event_card_description_visible(num)
            with check, allure.step(f"C58458: {event['title']} description is correct"):
                assert events_obj.get_event_card_description_text(num).strip() == event["summary"].strip()
            with check, allure.step(f"C58457: {event['title']} image is visible"):
                assert events_obj.is_event_card_image_visible(num)
            with check, allure.step(f"C58458: {event['title']} image is correct"):
                assert events_obj.get_event_card_image(num) == event["image"][0]
            with check, allure.step(f"C58457: {event['title']} date is visible"):
                assert events_obj.is_event_card_date_visible(num)
            with check, allure.step(f"C58458: {event['title']} date is correct"):
                expected_time = events_obj.get_formatted_time(event["start"], event["end"])
                assert events_obj.get_event_card_date_text(num) == expected_time
            num = num + 1
            if (num - 1) % 9 == 0:
                events_obj.scroll_to_pagination()
                events_obj.click_go_to_next_page_button()
                events_obj.scroll_to_events_section()
                num = 1
        driver.refresh()

    @severity(severity_level.NORMAL)
    @allure.feature('Events')
    @allure.title("Check for expired events")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58469", "C58469")
    @pytest.mark.dependency(depends=["test_1"])
    def test_5(self, driver):
        london_tz = pytz.timezone("Europe/London")
        now = datetime.now(london_tz)
        for event_id, event in self.event_list.items():
            end_date = datetime.fromisoformat(event['end'])
            with check, allure.step(f"C58469: {event['title']} is not expired"):
                assert end_date > now

    @severity(severity_level.NORMAL)
    @allure.feature('Events')
    @allure.title("Events are in chronological order")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58461", "C58461")
    @pytest.mark.dependency(depends=["test_1"])
    def test_6(self, driver):
        previous_start_date = None
        for event_id, event in self.event_list.items():
            start_date = datetime.fromisoformat(event['start'])
            if previous_start_date is not None:
                with check, allure.step(f"C58461: {event['title']} is in the correct order"):
                    assert start_date >= previous_start_date
            previous_start_date = start_date

    @severity(severity_level.NORMAL)
    @allure.feature('Events')
    @allure.title("Click on an event")
    @allure.issue("QP-267", "Story QP-267")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58459", "C58459")
    @pytest.mark.dependency(depends=["test_1"])
    def test_7(self, driver):
        events_obj = Events(driver)
        event_list = self.event_list
        event_ids = list(event_list.keys())
        random_id = random.choice(event_ids)
        while not events_obj.is_event_card_visible_by_title(event_list[random_id]["title"]):
            events_obj.scroll_to_pagination()
            events_obj.click_go_to_next_page_button()
            events_obj.scroll_to_events_section()
        events_obj.click_event_card_by_title(event_list[random_id]["title"])
        with check, allure.step(f"C58459: {event_list[random_id]['title']} info page is loaded"):
            assert events_obj.is_events_page_title_visible(event_list[random_id]['title'])
        events_obj.click_back_button()
        events_obj.scroll_to_events_section()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Events')
    @allure.title("Navigate to Event information page")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58484", "C58484")
    @pytest.mark.dependency(depends=["test_1"])
    @pytest.mark.dependency(name="test_8")
    def test_8(self, driver):
        events_obj = Events(driver)
        event_list = self.event_list
        event_ids = list(event_list.keys())
        TestEvents.event_without_booking_link, TestEvents.full_description_event = (
            events_obj.get_events_with_conditions(self.api_requests, event_ids))
        events_obj.scroll_to_events_section()
        while not events_obj.is_event_card_visible_by_title(self.full_description_event["title"]):
            events_obj.scroll_to_pagination()
            events_obj.click_go_to_next_page_button()
            events_obj.scroll_to_events_section()
        with check, allure.step(f"C58484: Click on event card"):
            events_obj.click_event_card_by_title(self.full_description_event['title'])
            events_obj.wait_individual_event_page_to_load()
            assert events_obj.is_events_page_title_visible(self.full_description_event['title'])

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Events')
    @allure.title("Event Information page appearance")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58485", "C58485")
    @pytest.mark.dependency(depends=["test_8"])
    def test_9(self, driver):
        events_obj = Events(driver)
        with check, allure.step(f"C58485: Event title is visible"):
            assert events_obj.is_events_page_title_visible(self.full_description_event["title"])
        with check, allure.step(f"C58485: Back button is visible"):
            assert events_obj.is_back_button_visible()
        with check, allure.step(f"C58485: Event date is visible"):
            assert events_obj.is_single_event_date_visible()
        with check, allure.step(f"C58485: Image section is visible"):
            assert events_obj.is_single_event_image_section_visible()
        with check, allure.step(f"C58485: About section is visible"):
            assert events_obj.is_single_event_about_section_visible()
        with check, allure.step(f"C58485: Opening times section is visible"):
            assert events_obj.is_single_event_opening_times_section_visible()
        with check, allure.step(f"C58485: Location section is visible"):
            assert events_obj.is_single_event_location_section_visible()
        with check, allure.step(f"C58485: Get directions link is visible"):
            assert events_obj.is_single_event_get_directions_link_visible()
        with check, allure.step(f"C58485: Add to calendar link is visible"):
            assert events_obj.is_single_event_add_to_calendar_link_visible()
        with check, allure.step(f"C58485: Buy tickets button is visible"):
            assert events_obj.is_buy_tickets_button_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Events')
    @allure.title("Event Images")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58487", "C58487")
    @pytest.mark.dependency(depends=["test_8"])
    def test_10(self, driver):
        events_obj = Events(driver)
        image_list = self.full_description_event["images"]
        for expected_image, actual_image in zip(image_list, events_obj.get_single_event_images()):
            with check, allure.step(f"C58487: {actual_image} is correct"):
                assert expected_image == actual_image

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Events')
    @allure.title("Event Title")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58488", "C58488")
    @pytest.mark.dependency(depends=["test_8"])
    def test_11(self, driver):
        events_obj = Events(driver)
        with check, allure.step(f"C58488: Event title is correct"):
            assert events_obj.get_individual_event_title_text() == self.full_description_event["title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Events')
    @allure.title("Event Date and Time")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58489", "C58489")
    @allure.testcase("58490", "C58490")
    @pytest.mark.dependency(depends=["test_8"])
    def test_12(self, driver):
        events_obj = Events(driver)
        with check, allure.step("C58489, C58490: Event date and time is correct"):
            start = self.full_description_event["start"]
            end = self.full_description_event["end"]
            expected_date = events_obj.get_formatted_time(start, end).strip()
            assert events_obj.get_single_event_date_text().strip() == expected_date

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Events')
    @allure.title("Event About section")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58492", "C58492")
    @pytest.mark.dependency(depends=["test_8"])
    def test_13(self, driver):
        events_obj = Events(driver)
        with check, allure.step("C58492: Event description is correct"):
            assert events_obj.get_single_event_about_section_text() == self.full_description_event["description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Events')
    @allure.title("Event Opening time section")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58494", "C58494")
    @pytest.mark.dependency(depends=["test_8"])
    def test_14(self, driver):
        events_obj = Events(driver)
        with check, allure.step("C58494: Event opening time is correct"):
            expected_opening_time = self.full_description_event["opening_times"]
            assert events_obj.get_single_event_opening_times_section_text() == expected_opening_time

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Events')
    @allure.title("Event Location section")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58496", "C58496")
    @pytest.mark.dependency(depends=["test_8"])
    def test_15(self, driver):
        events_obj = Events(driver)
        with check, allure.step("C58496: Event location is correct"):
            expected_location = self.full_description_event["address"]
            assert events_obj.get_single_event_location_section_text() == expected_location

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Events')
    @allure.title("Click Get Directions link")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58498", "C58498")
    @pytest.mark.dependency(depends=["test_8"])
    def test_16(self, driver):
        events_obj = Events(driver)
        original_handle = driver.window_handles[0]
        events_obj.click_single_event_get_directions_link(self.current_browser)
        for handle in driver.window_handles:
            if original_handle != handle:
                driver.switch_to.window(handle)
        url = driver.current_url
        with check, allure.step("C58496: User is navigated to Google Maps"):
            assert "https://www.google.com/maps" in url
        with check, allure.step("C58496: Site location is passed correctly"):
            assert self.full_description_event["location"] in url
        driver.close()
        driver.switch_to.window(original_handle)

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Events')
    @allure.title("Click Add to Calendar link")
    @allure.issue("QP-268", "Story QP-268")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58500", "C58500")
    @pytest.mark.dependency(depends=["test_8"])
    def test_17(self, driver):
        events_obj = Events(driver)
        download_dir = self.create_download_dir(self.current_browser)
        file_name = self.get_download_file_name(driver.current_url)
        file_path = os.path.join(download_dir, file_name)
        events_obj.click_single_event_add_to_calendar_link()

        cond = False
        for _ in range(10):
            if os.path.exists(file_path):
                cond = True
                break
            time.sleep(1)
        with check, allure.step("C58500: File is downloaded"):
            assert cond

        file_content = {}
        file = open(file_path, 'r')
        for line in file:
            line_content = line.split(":")
            if line_content[0] in list(file_content.keys()):
                file_content["INNER-" + line_content[0]] = line_content[1].replace("\n", "")
            else:
                file_content[line_content[0]] = line_content[1].replace("\n", "")

        print(file_content)

        with check, allure.step("C58500: Downloaded file is a valid ICS file"):
            assert file_content["BEGIN"] == "VCALENDAR"
        with check, allure.step("C58500: Events are available in the file"):
            assert file_content["INNER-BEGIN"] == "VEVENT"
        with check, allure.step("C58500: Correct event is passed"):
            assert file_content["SUMMARY"] == self.full_description_event["title"]

        self.cleanup_downloads(self.current_browser, download_dir, file_name)


