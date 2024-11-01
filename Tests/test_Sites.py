import allure
import pytest
import random
import re
from pytest_check import check
from allure import severity, severity_level

from Common.APIRequests import APIRequests
from Pages.HomePage import HomePage
from Pages.SitesPage import Sites, get_site_number, split_historic_and_retail_sites
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=0.5, rerun_except="assert")
class TestSites(BaseClass):
    current_browser = None

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestSites.current_browser = request.node.callspec.params["driver"]

    @classmethod
    def setup_class(cls):
        cls.api_requests = APIRequests()
        cls.site_list = cls.api_requests.get_sites_list()

    @severity(severity_level.CRITICAL)
    @allure.feature('Sites')
    @allure.title("User is navigated to the Sites page")
    def test_1(self, driver):
        home_page_obj = HomePage(driver)
        sites_obj = Sites(driver)
        driver.get(BaseClass.url)
        home_page_obj.wait_page_to_load(TestSites.current_browser)
        home_page_obj.click_sites_button()
        with check, allure.step("Sites title is visible"):
            assert sites_obj.is_sites_page_title_visible()

    @severity(severity_level.MINOR)
    @allure.feature('Sites')
    @allure.title("The historic tab is selected by default")
    def test_2(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("Historic tab is selected"):
            assert sites_obj.is_historic_tab_selected()
        with check, allure.step("Retail tab is not selected"):
            assert not sites_obj.is_retail_tab_selected()

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Check {site_type} sites")
    @pytest.mark.parametrize('site_type', ["Historic", "Retail"])
    def test_3(self, driver, site_type):
        sites_obj = Sites(driver)
        sites_obj.click_site_tab_button(site_type)
        site_list = self.site_list
        site_number = get_site_number(site_list, site_type)
        site_card_number = sites_obj.get_site_cards_number(site_type)
        filtered_site = split_historic_and_retail_sites(site_list, site_type)
        if site_number > 9:
            with check, allure.step("Nine cards are visible on the page"):
                assert site_card_number == 9
            with check, allure.step("Pagination is visible"):
                assert sites_obj.is_pagination_visible(site_type)
        else:
            with check, allure.step("The number of cards are visible on the page is correct"):
                assert site_card_number == site_number
            with check, allure.step("Pagination is not visible"):
                assert not sites_obj.is_pagination_visible(site_type)
        num = 1
        for site_id, site in filtered_site.items():
            title = site["title"]
            summary = site["summary"]
            with check, allure.step(f"{title} title is correct"):
                assert title.strip() == sites_obj.get_site_card_title(site_type, num).strip()
            with check, allure.step(f"{title} summary is correct"):
                assert summary.strip() == sites_obj.get_site_card_summary(site_type, num).strip()
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
    @pytest.mark.parametrize('site_type', ["Historic", "Retail"])
    def test_4(self, driver, site_type):
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
        for attribute in ["title", "summary", "address", "opening_hours", "description"]:
            text_method_name = f"get_individual_site_{attribute}_text"
            visible_method_name = f"is_individual_site_{attribute}_visible"
            if attribute == "title" or attribute == "summary":
                with check, allure.step(f"Check site {attribute}"):
                    actual_text = getattr(sites_obj, text_method_name)().strip()
                    expected_text = site_information[random_site_id][attribute].strip()
                    assert expected_text == actual_text
            else:
                if (site_information[random_site_id][attribute] is None
                        or (site_information[random_site_id][attribute] == "<p></p>" and attribute == "description")):
                    with check, allure.step(f"The field {attribute} is not visible"):
                        assert not getattr(sites_obj, visible_method_name)()
                else:
                    with check, allure.step(f"Check site {attribute}"):
                        actual_text = getattr(sites_obj, text_method_name)().strip().replace("\n", "")
                        expected_text = re.sub('<.*?>', '',
                                               site_information[random_site_id][attribute]
                                               .strip().replace('&quot;', '"').replace("&#x27;", "'")
                                               .split("</p><p>", 1)[0]).replace("\n", "")
                        assert expected_text == actual_text
        if site_information[random_site_id]["exhibit"] == {}:
            with check, allure.step("Exhibit section is missing"):
                assert not sites_obj.is_exhibit_section_visible()
        else:
            exhibits_number = len(site_information[random_site_id]["exhibit"])
            with check, allure.step("Check number of exhibit cards"):
                assert sites_obj.get_exhibit_cards_number() == exhibits_number
            num = 1
            for exhibit_id, exhibit in site_information[random_site_id]["exhibit"].items():
                title = exhibit["title"]
                summary = exhibit["summary"]
                with check, allure.step(f"{title} title is correct"):
                    assert title.strip() == sites_obj.get_exhibit_card_title(num).strip()
                with check, allure.step(f"{title} summary is correct"):
                    assert summary.strip() == sites_obj.get_exhibit_card_summary(num).strip()
                num = num + 1
        sites_obj.click_back_button()
        sites_obj.scroll_to_tab_buttons()
