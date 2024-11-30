import allure
import pytest
import random
from pytest_check import check
from allure import severity, severity_level
from Common.APIRequests import APIRequests
from Pages.AboutPage import AboutPage
from Pages.LoginPage import Login
from Pages.SitesPage import Sites, get_site_number, split_historic_and_retail_sites
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass
from Common.config import EMAIL, PASSWORD


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestSites(BaseClass):
    api_obj = None
    saved_sites = {}
    random_site_info = {}
    one_image_site = {}
    several_images_site = {}
    full_description_site = {}
    site_with_exhibits = {}
    site_without_exhibits = {}

    @classmethod
    def setup(cls):
        cls.saved_sites = {}
        TestSites.api_obj = APIRequests(cls.current_browser)
        saved_sites = TestSites.api_obj.get_saved_sites_list()
        if len(list(saved_sites.keys())) > 0:
            for site_id, site in saved_sites.items():
                TestSites.api_obj.unsave_site(site_id)

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
        site_list = self.site_list
        filtered_site = split_historic_and_retail_sites(site_list, site_type)
        site_ids = list(filtered_site.keys())
        random_id = random.choice(site_ids)
        site_information = self.api_requests.get_individual_site(random_id)
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button(site_type)
        while not sites_obj.is_site_card_visible_by_title(site_type, site_information[random_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(site_type, site_information[random_id]["title"])
        with check, allure.step(f"C{test_case}: {site_information[random_id]['title']} info page is loaded"):
            assert sites_obj.is_sites_page_title_visible(site_information[random_id]['title'])
        sites_obj.click_back_button()
        sites_obj.scroll_to_tab_buttons()

    @severity(severity_level.CRITICAL)
    @allure.feature('Sites')
    @allure.title("Saved sites for non logged user")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58737", "C58737")
    def test_9(self, driver):
        sites_obj = Sites(driver)
        self.setup()
        with check, allure.step("Saved sites button is not visible"):
            assert not sites_obj.is_saved_sites_button_visible()

    @severity(severity_level.CRITICAL)
    @allure.feature('Sites')
    @allure.title("Saved sites without saved sites")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58735", "C58735")
    def test_10(self, driver):
        sites_obj = Sites(driver)
        login_obj = Login(driver)
        main_nav_obj = MainNavigation(driver)
        email = EMAIL.replace("@", f"+{BaseClass.current_browser}@")
        login_obj.full_log_in(email, PASSWORD, BaseClass.current_browser)
        main_nav_obj.click_sites_button()
        main_nav_obj.wait_page_to_load()
        sites_obj.scroll_to_tab_buttons()
        with check, allure.step("C58735: Saved sites tab is visible"):
            assert sites_obj.is_saved_sites_button_visible()
        sites_obj.click_saved_sites_button()
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58735: Empty tab section is visible"):
            assert sites_obj.is_empty_tab_section_visible()

    @severity(severity_level.CRITICAL)
    @allure.feature('Sites')
    @allure.title("Saved sites with saved sites")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58736", "C58736")
    def test_11(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        site_list = self.site_list
        filtered_site = split_historic_and_retail_sites(site_list, "Historic")
        site_ids_list = list(filtered_site.keys())
        random_historic_site_id = random.choice(site_ids_list)
        filtered_site = split_historic_and_retail_sites(site_list, "Retail")
        site_ids_list = list(filtered_site.keys())
        random_retail_site_id = random.choice(site_ids_list)
        self.api_obj.save_site(random_historic_site_id)
        self.api_obj.save_site(random_retail_site_id)
        self.saved_sites[random_historic_site_id] = site_list[random_historic_site_id]
        self.saved_sites[random_retail_site_id] = site_list[random_retail_site_id]
        driver.refresh()
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58736: Saved sites cards are visible"):
            assert sites_obj.are_saved_sites_cards_visible()
        with check, allure.step("C58736: Saved sites cards number is correct"):
            assert sites_obj.get_saved_sites_cards_number() == 2

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Saved sites cards attributes")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58738", "C58738")
    def test_12(self, driver):
        sites_obj = Sites(driver)
        num = 1
        for site_id, site in self.saved_sites.items():
            with check, allure.step(f"C58738: {site['title']} title is visible"):
                assert sites_obj.is_site_card_title_visible("savedSites", num)
            with check, allure.step(f"C58738: {site['title']} summary is visible"):
                assert sites_obj.is_site_card_summary_visible("savedSites", num)
            with check, allure.step(f"C58738: {site['title']} image is visible"):
                assert sites_obj.is_site_card_image_visible("savedSites", num)
            with check, allure.step(f"C58738: {site['title']} saved site icon is visible"):
                assert sites_obj.is_saved_site_icon_visible("savedSites", site['title'])
            num = num + 1

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Correct saved sites cards are presented")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58739", "C58739")
    @allure.testcase("58741", "C58741")
    def test_13(self, driver):
        sites_obj = Sites(driver)
        titles, summaries, images = [], [], []
        for site_id, site in self.saved_sites.items():
            titles.append(site["title"].strip())
            summaries.append(site["summary"].replace("\n", "").strip())
            images.append(site["image"])
        card_number = sites_obj.get_saved_sites_cards_number()
        for i in range(card_number):
            actual_title = sites_obj.get_site_card_title("savedSites", i + 1).strip()
            with check, allure.step(f"C58739: {actual_title} title is correct"):
                assert actual_title in titles
            actual_summary = sites_obj.get_site_card_summary("savedSites", i + 1).strip()
            with check, allure.step(f"C58741: {actual_title} summary is correct"):
                assert actual_summary in summaries
            actual_image = sites_obj.get_site_card_image("savedSites", i + 1).strip()
            with check, allure.step(f"C58741: {actual_title} image is correct"):
                assert actual_image in images

    @severity(severity_level.CRITICAL)
    @allure.feature('Sites')
    @allure.title("Click on saved site card")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58740", "C58740")
    def test_14(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        saved_sites_ids = list(self.saved_sites.keys())
        random_saved_site_id = random.choice(saved_sites_ids)
        random_saved_site_title = self.saved_sites[random_saved_site_id]["title"]
        sites_obj.click_site_card_by_title("savedSites", random_saved_site_title)
        main_nav_obj.wait_page_to_load()
        with check, allure.step(f"C58740: User is navigated to the {random_saved_site_title} site page"):
            assert sites_obj.is_sites_page_title_visible(random_saved_site_title)
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()
        sites_obj.scroll_to_tab_buttons()

    @severity(severity_level.NORMAL)
    @allure.feature('Sites')
    @allure.title("Saved site icon on site cards")
    @allure.issue("QP-383", "Story QP-383")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58742", "C58742")
    @pytest.mark.parametrize('site_type', ["Historic", "Retail"])
    def test_15(self, driver, site_type):
        sites_obj = Sites(driver)
        sites_obj.click_site_tab_button(site_type)
        site_list = self.site_list
        saved_sites_titles = []
        for site_id, site in self.saved_sites.items():
            saved_sites_titles.append(site["title"].strip())
        filtered_site = split_historic_and_retail_sites(site_list, site_type)
        num = 1
        for site_id, site in filtered_site.items():
            title = site["title"].strip()
            if title in saved_sites_titles:
                with check, allure.step("C58742: Site card has a saved site icon"):
                    assert sites_obj.is_saved_site_icon_visible(site_type, title)
            else:
                with check, allure.step("C58742: Site card does not have a saved site icon"):
                    assert not sites_obj.is_saved_site_icon_visible(site_type, title)
            num = num + 1
            if (num - 1) % 9 == 0:
                sites_obj.scroll_to_pagination()
                sites_obj.click_next_pagination_button()
                sites_obj.scroll_to_tab_buttons()
                num = 1
        driver.refresh()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Navigate to Site Information page")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58409", "C58409")
    @pytest.mark.dependency(name="test_16")
    def test_16(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        site_list = self.site_list
        sites_ids = []
        filtered_site = split_historic_and_retail_sites(site_list, "Historic")
        for site_id, site in filtered_site.items():
            sites_ids.append(site_id)
        random_site_id = random.choice(sites_ids)
        random_site_title = site_list[random_site_id]["title"]
        TestSites.random_site_info = self.api_obj.get_individual_site(random_site_id)
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button("Historic")
        while not sites_obj.is_site_card_visible_by_title("Historic", random_site_title):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        with check, allure.step("C58409: Click on a site card"):
            sites_obj.click_site_card_by_title("Historic", random_site_title)
            main_nav_obj.wait_page_to_load()
            assert sites_obj.is_sites_page_title_visible(random_site_title)

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Site Information page appearance")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58410", "C58410")
    @pytest.mark.dependency(depends=["test_16"])
    def test_17(self, driver):
        sites_obj = Sites(driver)
        random_site_info = self.random_site_info
        with check, allure.step("C58410: Back button is visible"):
            assert sites_obj.is_back_button_visible()
        with check, allure.step("C58410: Image section is visible"):
            assert sites_obj.is_single_site_image_section_visible()
        site_id = list(random_site_info.keys())
        if len(list(random_site_info[site_id[0]]["exhibit"].keys())) != 0:
            with check, allure.step("C58410: Exhibits section is visible"):
                assert sites_obj.is_exhibit_section_visible()
        else:
            with check, allure.step("C58410: Exhibits section is not visible"):
                assert not sites_obj.is_exhibit_section_visible()
        with check, allure.step("C58410: Travel section is visible"):
            assert sites_obj.is_single_site_travel_section_visible()
        with check, allure.step("C58410: Footer is visible"):
            assert sites_obj.is_single_site_footer_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Click back button")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58412", "C58412")
    @pytest.mark.dependency(depends=["test_16"])
    def test_18(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58412: Sites page is loaded"):
            assert sites_obj.is_sites_page_title_visible(self.sites_page_content["heading_title"])

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Site with only one photo")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58411", "C58411")
    def test_19(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        about_obj = AboutPage(driver)
        site_list = self.site_list
        sites_ids = list(site_list.keys())
        (TestSites.one_image_site, TestSites.several_images_site,
         TestSites.full_description_site, TestSites.site_with_exhibits,
         TestSites.site_without_exhibits) = sites_obj.get_sites_with_conditions(self.api_obj, sites_ids)
        if len(list(self.one_image_site.keys())) == 0:
            pytest.skip("No sites available with only 1 image")
        one_image_site_id = list(self.one_image_site.keys())[0]
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button(self.one_image_site[one_image_site_id]["type"])
        while not sites_obj.is_site_card_visible_by_title(self.one_image_site[one_image_site_id]["type"],
                                                          self.one_image_site[one_image_site_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(self.one_image_site[one_image_site_id]["type"],
                                           self.one_image_site[one_image_site_id]["title"])
        main_nav_obj.wait_page_to_load()
        sites_obj.scroll_to_single_site_image_section()
        with check, allure.step("C58411: Next image button is not visible"):
            assert not about_obj.is_next_slide_button_visible()
        with check, allure.step("C58411: Scroll bar is not visible"):
            assert not about_obj.is_image_carousel_scroll_visible()
        with check, allure.step("C58411: Only one image is visible"):
            assert len(about_obj.get_images()) == 1
        with check, allure.step("C58522: The correct image is displayed"):
            assert about_obj.get_images()[0] == self.one_image_site[one_image_site_id]["images"][0]
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Site with more than one photo")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58413", "C58413")
    def test_20(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        about_obj = AboutPage(driver)
        if len(list(self.several_images_site.keys())) == 0:
            pytest.skip("No sites available with several images")
        site_id = list(self.several_images_site.keys())[0]
        if sites_obj.is_heading_description_visible():
            sites_obj.scroll_to_tab_buttons()
            sites_obj.click_site_tab_button(self.several_images_site[site_id]["type"])
            while not sites_obj.is_site_card_visible_by_title(self.several_images_site[site_id]["type"],
                                                              self.several_images_site[site_id]["title"]):
                sites_obj.scroll_to_pagination()
                sites_obj.click_next_pagination_button()
                sites_obj.scroll_to_tab_buttons()
            sites_obj.click_site_card_by_title(self.several_images_site[site_id]["type"],
                                               self.several_images_site[site_id]["title"])
            main_nav_obj.wait_page_to_load()
        sites_obj.scroll_to_single_site_image_section()
        image_list = about_obj.get_images()
        i = 0
        for image in image_list:
            with check, allure.step(f"C58413: The image {image} is correct"):
                assert image == self.several_images_site[site_id]["images"][i]
            i = i + 1
        with check, allure.step("C58413: Next image button is visible"):
            assert about_obj.is_next_slide_button_visible()
        with check, allure.step("C58413: Scroll bar is visible"):
            assert about_obj.is_image_carousel_scroll_visible()
        driver.refresh()

    @severity(severity_level.MINOR)
    @allure.feature('Individual Sites')
    @allure.title("Scroll images with buttons")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58414", "C58414")
    def test_21(self, driver):
        about_obj = AboutPage(driver)
        with check, allure.step("C58414: Initially next is visible and previous is not"):
            assert about_obj.is_next_slide_button_visible() and not about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58414: Carousel position is at the start"):
            assert about_obj.get_image_carousel_position() == "start"
        with check, allure.step("C58414: Next and previous buttons after clicking next"):
            about_obj.click_next_slide_button()
            assert about_obj.is_next_slide_button_visible() and about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58414: Carousel position is at the middle"):
            assert about_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58414: Next and previous buttons at the end of the carousel"):
            position = about_obj.get_image_carousel_position()
            while position != "end":
                about_obj.click_next_slide_button()
                position = about_obj.get_image_carousel_position()
            assert not about_obj.is_next_slide_button_visible() and about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58414: Carousel position is at the end"):
            assert about_obj.get_image_carousel_position() == "end"
        with check, allure.step("C58414: Next and previous buttons after clicking previous"):
            about_obj.click_previous_slide_button()
            assert about_obj.is_next_slide_button_visible() and about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58414: Carousel position is at the middle"):
            assert about_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58414: Next and previous buttons at the start of the carousel"):
            position = about_obj.get_image_carousel_position()
            while position != "start":
                about_obj.click_previous_slide_button()
                position = about_obj.get_image_carousel_position()
            assert about_obj.is_next_slide_button_visible() and not about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58414: Carousel position is at the start"):
            assert about_obj.get_image_carousel_position() == "start"

    @severity(severity_level.MINOR)
    @allure.feature('Individual Sites')
    @allure.title("Scroll trough images")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58415", "C58415")
    def test_22(self, driver):
        about_obj = AboutPage(driver)
        with check, allure.step("C58415: Initially next is visible and previous is not"):
            assert about_obj.is_next_slide_button_visible() and not about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58415: Carousel position is at the start"):
            assert about_obj.get_image_carousel_position() == "start"
        with check, allure.step("C58415: Next and previous buttons after scrolling"):
            about_obj.scroll_right_in_image_gallery()
            assert about_obj.is_next_slide_button_visible() and about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58415: Carousel position is at the middle"):
            assert about_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58415: Next and previous buttons at the end of the carousel"):
            position = about_obj.get_image_carousel_position()
            while position != "end":
                about_obj.scroll_right_in_image_gallery()
                position = about_obj.get_image_carousel_position()
            assert not about_obj.is_next_slide_button_visible() and about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58415: Carousel position is at the end"):
            assert about_obj.get_image_carousel_position() == "end"
        with check, allure.step("C58415: Next and previous buttons after scrolling left"):
            about_obj.scroll_left_in_image_gallery()
            assert about_obj.is_next_slide_button_visible() and about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58415: Carousel position is at the middle"):
            assert about_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58415: Next and previous buttons at the start of the carousel"):
            position = about_obj.get_image_carousel_position()
            while position != "start":
                about_obj.scroll_left_in_image_gallery()
                position = about_obj.get_image_carousel_position()
            assert about_obj.is_next_slide_button_visible() and not about_obj.is_previous_slide_button_visible()
        with check, allure.step("C58415: Carousel position is at the start"):
            assert about_obj.get_image_carousel_position() == "start"

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information appearance")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58416", "C58416")
    @pytest.mark.dependency(name="test_23")
    def test_23(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()
        if len(list(self.full_description_site.keys())) == 0:
            pytest.skip("No sites available with full description")
        site_id = list(self.full_description_site.keys())[0]
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button(self.full_description_site[site_id]["type"])
        while not sites_obj.is_site_card_visible_by_title(self.full_description_site[site_id]["type"],
                                                          self.full_description_site[site_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(self.full_description_site[site_id]["type"],
                                           self.full_description_site[site_id]["title"])
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58416: Section title is visible"):
            assert sites_obj.is_sites_page_title_visible(self.full_description_site[site_id]["title"])
        with check, allure.step("C58416: Section summary is visible"):
            assert sites_obj.is_single_site_summary_visible()
        with check, allure.step("C58416: About section is visible"):
            assert sites_obj.is_single_site_about_visible()
        with check, allure.step("C58416: Opening times section is visible"):
            assert sites_obj.is_single_site_opening_times_visible()
        with check, allure.step("C58416: Location section is visible"):
            assert sites_obj.is_single_site_location_visible()
        with check, allure.step("C58416: Amenities section is visible"):
            assert sites_obj.is_single_site_amenities_visible()
        with check, allure.step("C58416: Get directions link is visible"):
            assert sites_obj.is_single_site_get_directions_link_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information section title")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58417", "C58417")
    @pytest.mark.dependency(depends=["test_23"])
    def test_24(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58417: Section title is correct"):
            site_id = list(self.full_description_site.keys())[0]
            assert sites_obj.get_individual_site_title_text() == self.full_description_site[site_id]["title"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information section summary")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58418", "C58418")
    @pytest.mark.dependency(depends=["test_23"])
    def test_25(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58418: Section summary is correct"):
            site_id = list(self.full_description_site.keys())[0]
            assert sites_obj.get_single_site_summary_text() == self.full_description_site[site_id]["summary"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information about section")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58419", "C58419")
    @pytest.mark.dependency(depends=["test_23"])
    def test_26(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58419: About section is correct"):
            site_id = list(self.full_description_site.keys())[0]
            assert sites_obj.get_single_site_about_text() == self.full_description_site[site_id]["description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information opening times section")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58420", "C58420")
    @pytest.mark.dependency(depends=["test_23"])
    def test_27(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58420: Opening times section is correct"):
            s_id = list(self.full_description_site.keys())[0]
            assert sites_obj.get_single_site_opening_times_text() == self.full_description_site[s_id]["opening_hours"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information location section")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58421", "C58421")
    @pytest.mark.dependency(depends=["test_23"])
    def test_28(self, driver):
        sites_obj = Sites(driver)
        with check, allure.step("C58421: Location section is correct"):
            site_id = list(self.full_description_site.keys())[0]
            assert sites_obj.get_single_site_location_text() == self.full_description_site[site_id]["address"]

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Site information amenities section")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58425", "C58425")
    @pytest.mark.dependency(depends=["test_23"])
    def test_29(self, driver):
        sites_obj = Sites(driver)
        site_id = list(self.full_description_site.keys())[0]
        amenity_list = sites_obj.get_single_site_amenities_list()
        for amenity in amenity_list:
            with check, allure.step(f"C58425: {amenity} amenity is correct"):
                assert amenity in self.full_description_site[site_id]["facilities"]

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Click on Get Directions link")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58422", "C58422")
    @pytest.mark.dependency(depends=["test_23"])
    def test_30(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        site_id = list(self.full_description_site.keys())[0]
        original_handle = driver.window_handles[0]
        sites_obj.click_single_site_get_directions_link(self.current_browser)
        if self.current_browser == "safari":
            for handle in driver.window_handles:
                if original_handle != handle:
                    driver.switch_to.window(handle)
        else:
            driver.switch_to.window(driver.window_handles[1])
        url = driver.current_url
        with check, allure.step("C58422: User is navigated to Google Maps"):
            assert "https://www.google.com/maps" in url
        with check, allure.step("C58422: Site location is passed correctly"):
            assert self.full_description_site[site_id]["location"] in url
        if self.current_browser == "safari":
            for handle in driver.window_handles:
                if original_handle != handle:
                    driver.switch_to.window(handle)
            driver.close()
            driver.switch_to.window(original_handle)
        else:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Site with no exhibits")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58427", "C58427")
    def test_31(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        if len(list(self.site_without_exhibits.keys())) == 0:
            pytest.skip("No sites available without exhibits")
        site_id = list(self.site_without_exhibits.keys())[0]
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button(self.site_without_exhibits[site_id]["type"])
        while not sites_obj.is_site_card_visible_by_title(self.site_without_exhibits[site_id]["type"],
                                                          self.site_without_exhibits[site_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(self.site_without_exhibits[site_id]["type"],
                                           self.site_without_exhibits[site_id]["title"])
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58427: Exhibit section is not visible"):
            assert not sites_obj.is_single_site_exhibit_section_visible()
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Site with exhibits")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58426", "C58426")
    @pytest.mark.dependency(name="test_32")
    def test_32(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        if len(list(self.site_with_exhibits.keys())) == 0:
            pytest.skip("No sites available with exhibits")
        site_id = list(self.site_with_exhibits.keys())[0]
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button(self.site_with_exhibits[site_id]["type"])
        while not sites_obj.is_site_card_visible_by_title(self.site_with_exhibits[site_id]["type"],
                                                          self.site_with_exhibits[site_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(self.site_with_exhibits[site_id]["type"],
                                           self.site_with_exhibits[site_id]["title"])
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58426: Exhibit section is visible"):
            assert sites_obj.is_single_site_exhibit_section_visible()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Presented exhibits")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58428", "C58428")
    @pytest.mark.dependency(depends=["test_32"])
    def test_33(self, driver):
        sites_obj = Sites(driver)
        sites_obj.scroll_to_exhibit_section()
        site_id = list(self.site_with_exhibits.keys())[0]
        expected_exhibits = self.site_with_exhibits[site_id]["exhibit"]
        with check, allure.step("C58428: The exhibits number is correct"):
            assert sites_obj.get_single_site_exhibit_cards_number() == len(list(expected_exhibits.keys()))
        i = 0
        for exhibit_id, exhibit in expected_exhibits.items():
            with check, allure.step(f"C58428: {exhibit['title']} title is correct"):
                assert sites_obj.get_single_site_exhibit_title(i) == exhibit['title']
            with check, allure.step(f"C58428: {exhibit['title']} description is correct"):
                assert sites_obj.get_single_site_exhibit_summary(i) == exhibit['summary']
            with check, allure.step(f"C58428: {exhibit['title']} image is correct"):
                assert sites_obj.get_single_site_exhibit_image(i) == exhibit['image']
            i = i + 1

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Exhibit cards are not clickable")
    @allure.issue("QP-264", "Story QP-264")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58429", "C58429")
    @pytest.mark.dependency(depends=["test_32"])
    def test_34(self, driver):
        sites_obj = Sites(driver)
        site_id = list(self.site_with_exhibits.keys())[0]
        exhibits = self.site_with_exhibits[site_id]["exhibit"]
        i = 0
        for exhibit_id, exhibit in exhibits.items():
            with check, allure.step(f"C58429: {exhibit['title']} is not clickable"):
                assert not sites_obj.is_single_site_exhibit_card_clickable(i)
            i = i + 1
        sites_obj.click_back_button()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Save site button for logged user")
    @allure.issue("QP-283", "Story QP-283")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58743", "C58743")
    def test_35(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        site_list = self.site_list
        site_ids = list(site_list.keys())
        saved_ids = list(self.saved_sites.keys())
        random_id = random.choice(site_ids)
        while random_id in saved_ids:
            random_id = random.choice(site_ids)
        TestSites.random_site_info = self.api_obj.get_individual_site(random_id)
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_tab_button(self.random_site_info[random_id]["type"])
        while not sites_obj.is_site_card_visible_by_title(self.random_site_info[random_id]["type"],
                                                          self.random_site_info[random_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(self.random_site_info[random_id]["type"],
                                           self.random_site_info[random_id]["title"])
        main_nav_obj.wait_page_to_load()
        with check, allure.step("C58743: Save site button is visible"):
            assert sites_obj.is_save_site_button_visible()
        with check, allure.step("C58743: Save site button is not filled"):
            assert not sites_obj.is_save_site_icon_filled()

    @severity(severity_level.BLOCKER)
    @allure.feature('Individual Sites')
    @allure.title("Click save site button")
    @allure.issue("QP-283", "Story QP-283")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58745", "C58745")
    def test_36(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        sites_obj.click_save_site_button()
        with check, allure.step("C58745: Save site button is filled"):
            assert sites_obj.is_save_site_icon_filled()
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Saved site is visible in the saved site section")
    @allure.issue("QP-283", "Story QP-283")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58746", "C58746")
    def test_37(self, driver):
        sites_obj = Sites(driver)
        sites_obj.scroll_to_tab_buttons()
        sites_obj.click_saved_sites_button()
        site_id = list(self.random_site_info.keys())[0]
        with check, allure.step(f"C58746: Site {self.random_site_info[site_id]['title']} is visible in the section"):
            assert sites_obj.is_site_card_visible_by_title(self.random_site_info[site_id]['type'],
                                                           self.random_site_info[site_id]['title'])

    @severity(severity_level.CRITICAL)
    @allure.feature('Individual Sites')
    @allure.title("Saved site is visible in the mobile app")
    @allure.issue("QP-283", "Story QP-283")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58747", "C58747")
    def test_38(self, driver):
        saved_sites = self.api_obj.get_saved_sites_list()
        saved_sites_titles = []
        for site_id, site in saved_sites.items():
            saved_sites_titles.append(site["title"])
        site_id = list(self.random_site_info.keys())[0]
        with check, allure.step(f"C58747: Site {self.random_site_info[site_id]['title']} is visible"):
            assert self.random_site_info[site_id]['title'] in saved_sites_titles

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Unsave a site")
    @allure.issue("QP-283", "Story QP-283")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58748", "C58748")
    def test_39(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        site_id = list(self.random_site_info.keys())[0]
        sites_obj.click_site_card_by_title("savedSites", self.random_site_info[site_id]["title"])
        sites_obj.click_save_site_button()
        with check, allure.step(f"C58748: Save site icon is not filled"):
            assert not sites_obj.is_save_site_icon_filled()
        sites_obj.click_back_button()
        main_nav_obj.wait_page_to_load()
        with check, allure.step(f"C58748: Site is not visible in the saved sites section"):
            assert not sites_obj.is_site_card_visible_by_title("savedSites",
                                                               self.random_site_info[site_id]["title"])

    @severity(severity_level.NORMAL)
    @allure.feature('Individual Sites')
    @allure.title("Save site button for non logged user")
    @allure.issue("QP-283", "Story QP-283")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58744", "C58744")
    def test_40(self, driver):
        sites_obj = Sites(driver)
        main_nav_obj = MainNavigation(driver)
        main_nav_obj.click_logout_button()
        main_nav_obj.wait_page_to_load()
        main_nav_obj.click_sites_button()
        sites_obj.scroll_to_tab_buttons()
        site_id = list(self.random_site_info.keys())[0]
        sites_obj.click_site_tab_button(self.random_site_info[site_id]["type"])
        while not sites_obj.is_site_card_visible_by_title(self.random_site_info[site_id]["type"],
                                                          self.random_site_info[site_id]["title"]):
            sites_obj.scroll_to_pagination()
            sites_obj.click_next_pagination_button()
            sites_obj.scroll_to_tab_buttons()
        sites_obj.click_site_card_by_title(self.random_site_info[site_id]["type"],
                                           self.random_site_info[site_id]["title"])
        main_nav_obj.wait_page_to_load()
        with check, allure.step(f"C58744: Save site button is not visible"):
            assert not sites_obj.is_save_site_button_visible()
