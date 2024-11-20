import allure
import pytest
import random
import re
from pytest_check import check
from allure import severity, severity_level
from Pages.SitesPage import Sites, get_site_number, split_historic_and_retail_sites
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestSites(BaseClass):
    current_browser = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestSites.current_browser = request.node.callspec.params["driver"]

    @severity(severity_level.CRITICAL)
    @allure.feature('Sites')
    @allure.title("User is navigated to the Sites page")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58327", "C58327")
    @pytest.mark.dependency(name="test_1")
    def test_1(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(self.url)
        main_nav_obj.wait_page_to_load()
        main_nav_obj.click_sites_button()
        with check, allure.step("C58327: Sites page is loaded"):
            assert sites_obj.is_sites_page_title_visible(self.sites_page_content["heading_title"])

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check the welcome message appearance")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58352", "C58352")
    @pytest.mark.dependency(depends=["test_1"])
    def test_2(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58352: Heading title is visible"):
            assert sites_obj.is_sites_page_title_visible(self.sites_page_content["heading_title"])
        with check, allure.step("C58352: Heading description is visible"):
            assert sites_obj.is_heading_description_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check the welcome message text")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58353", "C58353")
    @pytest.mark.dependency(depends=["test_1"])
    def test_3(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58353: Heading title text is correct"):
            assert sites_obj.get_heading_title_text() == self.sites_page_content["heading_title"]
        with check, allure.step("C58353: Heading description text is correct"):
            assert sites_obj.get_heading_description_text() == self.sites_page_content["heading_description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check the site tabs title")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58354", "C58354")
    @pytest.mark.dependency(depends=["test_1"])
    def test_4(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58354: Section title text is correct"):
            assert sites_obj.get_app_tabs_title_text() == self.sites_page_content["section_title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check the site tabs description")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58408", "C58408")
    @pytest.mark.dependency(depends=["test_1"])
    def test_5(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58408: Section description text is correct"):
            assert sites_obj.get_app_tabs_description_text() == self.sites_page_content["section_description"]

    @severity(severity_level.MINOR)
    @allure.feature('Sites')
    @allure.title("The historic tab is selected by default")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @pytest.mark.dependency(depends=["test_1"])
    def test_6(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("Historic tab is selected"):
            assert sites_obj.is_historic_tab_selected()
        with check, allure.step("Retail tab is not selected"):
            assert not sites_obj.is_retail_tab_selected()

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check {site_type} sites")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58355", "C58355")
    @allure.testcase("58356", "C58356")
    @allure.testcase("58357", "C58357")
    @allure.testcase("58359", "C58359")
    @allure.testcase("58360", "C58360")
    @allure.testcase("58361", "C58361")
    @allure.testcase("58399", "C58399")
    @allure.testcase("58396", "C58396")
    @pytest.mark.parametrize('site_type, test_case', [
        ("Historic", ["58355", "58356", "58357", "58399"]),
        ("Retail", ["58359", "58360", "58361", "58396"])
    ])
    def test_7(self, driver, site_type, test_case):
        sites_obj = Sites(driver)
        sites_obj.click_site_tab_button(site_type)
        site_list = self.site_list
        site_number = get_site_number(site_list, site_type)
        site_card_number = sites_obj.get_site_cards_number(site_type)
        filtered_site = split_historic_and_retail_sites(site_list, site_type)
        if site_number > 9:
            with check, allure.step(f"C{test_case[0]}: Nine cards are visible on the page"):
                assert site_card_number == 9
            with check, allure.step(f"C{test_case[0]}: Pagination is visible"):
                assert sites_obj.is_pagination_visible(site_type)
        else:
            with check, allure.step(f"C{test_case[0]}: The number of cards are visible on the page is correct"):
                assert site_card_number == site_number
            with check, allure.step(f"C{test_case[0]}: Pagination is not visible"):
                assert not sites_obj.is_pagination_visible(site_type)
        num = 1
        for site_id, site in filtered_site.items():
            title = site["title"]
            summary = site["summary"]
            image = site["image"]
            with check, allure.step(f"C{test_case[1]}: {title} title is visible"):
                assert sites_obj.is_site_card_title_visible(site_type, num)
            with check, allure.step(f"C{test_case[1]}: {title} summary is visible"):
                assert sites_obj.is_site_card_summary_visible(site_type, num)
            with check, allure.step(f"C{test_case[1]}: {title} image is visible"):
                assert sites_obj.is_site_card_image_visible(site_type, num)
            with check, allure.step(f"C{test_case[2]}: {title} title is correct"):
                assert title.strip() == sites_obj.get_site_card_title(site_type, num).strip()
            with check, allure.step(f"C{test_case[3]}: {title} summary is correct"):
                assert summary.strip() == sites_obj.get_site_card_summary(site_type, num).strip()
            with check, allure.step(f"C{test_case[3]}: {title} image is correct"):
                assert image.strip() == sites_obj.get_site_card_image(site_type, num).strip()
            num = num + 1
            if (num - 1) % 9 == 0:
                sites_obj.scroll_to_pagination()
                sites_obj.click_next_pagination_button()
                sites_obj.scroll_to_tab_buttons()
                num = 1
        driver.refresh()

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check individual {site_type} site")
    @allure.issue("QP-263", "Story QP-263")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58358", "C58358")
    @allure.testcase("58366", "C58366")
    @pytest.mark.parametrize('site_type, test_case', [("Historic", "58358"), ("Retail", "58366")])
    def test_8(self, driver, site_type, test_case):
        sites_obj = Sites(driver)
        sites_obj.click_site_tab_button(site_type)
        site_list = self.site_list
        filtered_site = split_historic_and_retail_sites(site_list, site_type)
        site_ids_list = list(filtered_site.keys())
        first_elements = list(enumerate(site_ids_list[:9]))
        position, random_site_id = random.choice(first_elements)
        site_information = self.api_requests.get_individual_site(random_site_id)
        sites_obj.click_site_card(site_type, position)
        sites_obj.wait_individual_site_page_to_load()
        with check, allure.step(f"C{test_case}: {site_information[random_site_id]['title']} info page is loaded"):
            assert sites_obj.is_sites_page_title_visible(site_information[random_site_id]['title'])
        # for attribute in ["title", "summary", "address", "opening_hours", "description"]:
        #     text_method_name = f"get_individual_site_{attribute}_text"
        #     visible_method_name = f"is_individual_site_{attribute}_visible"
        #     if attribute == "title" or attribute == "summary":
        #         with check, allure.step(f"Check site {attribute}"):
        #             actual_text = getattr(sites_obj, text_method_name)().strip()
        #             expected_text = site_information[random_site_id][attribute].strip()
        #             assert expected_text == actual_text
        #     else:
        #         if (site_information[random_site_id][attribute] is None
        #                 or (site_information[random_site_id][attribute] == "<p></p>" and attribute == "description")):
        #             with check, allure.step(f"The field {attribute} is not visible"):
        #                 assert not getattr(sites_obj, visible_method_name)()
        #         else:
        #             with check, allure.step(f"Check site {attribute}"):
        #                 actual_text = getattr(sites_obj, text_method_name)().strip().replace("\n", "")
        #                 expected_text = re.sub('<.*?>', '',
        #                                        site_information[random_site_id][attribute]
        #                                        .strip().replace('&quot;', '"').replace("&#x27;", "'")
        #                                        .split("</p><p>", 1)[0]).replace("\n", "")
        #                 assert expected_text == actual_text
        # if site_information[random_site_id]["exhibit"] == {}:
        #     with check, allure.step("Exhibit section is missing"):
        #         assert not sites_obj.is_exhibit_section_visible()
        # else:
        #     exhibits_number = len(site_information[random_site_id]["exhibit"])
        #     with check, allure.step("Check number of exhibit cards"):
        #         assert sites_obj.get_exhibit_cards_number() == exhibits_number
        #     num = 1
        #     for exhibit_id, exhibit in site_information[random_site_id]["exhibit"].items():
        #         title = exhibit["title"]
        #         summary = exhibit["summary"]
        #         with check, allure.step(f"{title} title is correct"):
        #             assert title.strip() == sites_obj.get_exhibit_card_title(num).strip()
        #         with check, allure.step(f"{title} summary is correct"):
        #             assert summary.strip() == sites_obj.get_exhibit_card_summary(num).strip()
        #         num = num + 1
        sites_obj.click_back_button()
        sites_obj.scroll_to_tab_buttons()

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Saved sites for non logged user")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58737", "C58737")
    def test_9(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("Saved sites button is not visible"):
            assert not sites_obj.is_saved_sites_button_visible()
