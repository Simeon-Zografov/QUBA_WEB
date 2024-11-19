import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.Admin import Admin
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass
from Pages.SponsorsPage import SponsorsPage


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestSponsorsPage(BaseClass):
    current_browser = None
    # sponsors_page_content = {'heading_title': 'Historical city exploration experiences sponsored by leaders in travel innovation ', 'heading_description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla scelerisque, sem vitae semper bibendum, tellus ligula vestibulum est, sit amet molestie augue magna nec nulla.', 'logos': ['abstract-tree-life-logo-botanical-600nw-2441085421.webp', 'Shell-Logo-Design.webp', 'compressed_35430be975609459d82adc065ae68481.webp', 'amazon.png', 'download.png', 'images (1).png', 'images (2).png'], 'benefits_title': 'Get involved in building tomorrow ', 'benefits_description': 'We believe in pushing boundaries and achieving greatness. As a sponsor, you’ll not only have the unique opportunity to support our mission but also to engage with a dynamic and passionate community that values dedication, perseverance, and excellence.Why Sponsor Us?Brand Visibility: Showcase your brand to a large and diverse audience through our events, digital channels, and media coverage.Community Impact: Be part of a positive initiative that encourages growth, teamwork, and success.Exclusive Benefits: Enjoy premium access, VIP experiences, and personalized branding opportunities at all our events.', 'benefits_link_text': 'Get in touch', 'benefits_link_url': '/contact', 'themes_titles': ['Sponsor benefit', 'Sponsor benefit', 'Sponsor benefit'], 'themes_descriptions': ['Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla scelerisque, sem vitae semper bibendum, tellus ligula vestibulum est, sit amet molestie augue magna nec nulla.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce blandit sollicitudin nunc. Cras justo odio, dapibus ac facilisis in, egestas eget quam.', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce blandit sollicitudin nunc. Cras justo odio, dapibus ac facilisis in, egestas eget quam.']}

    sponsors_page_content = {}

    @pytest.fixture(autouse=True)
    def setup(self, request):
        TestSponsorsPage.current_browser = request.node.callspec.params["driver"]

    @pytest.fixture(scope="class", autouse=True)
    def get_sponsors_page_content(self, driver):
        admin_obj = Admin(driver)
        admin_obj.switch_to_admin()
        TestSponsorsPage.sponsors_page_content = admin_obj.get_sponsors_page_content()
        print(TestSponsorsPage.sponsors_page_content)
        admin_obj.close_admin()

    @severity(severity_level.CRITICAL)
    @allure.feature('Sponsors page')
    @allure.title("User is navigated to the Sponsors page")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58557", "C58557")
    @pytest.mark.dependency(name="test_1")
    def test_1(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(BaseClass.url)
        main_nav_obj.click_sponsors_button()
        with check, allure.step("C58557: Check the page title"):
            assert sponsors_page_obj.is_sponsors_page_title_visible(TestSponsorsPage.sponsors_page_content["heading_title"])

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Sponsors page welcome message appearance")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58597", "C58597")
    @pytest.mark.dependency(depends=["test_1"])
    def test_2(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        with check, allure.step("C58597: Sponsors page heading title is visible"):
            assert sponsors_page_obj.is_heading_title_visible()
        with check, allure.step("C58597: Sponsors page heading description is visible"):
            assert sponsors_page_obj.is_heading_description_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Sponsors page welcome message text")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58598", "C58598")
    @pytest.mark.dependency(depends=["test_1"])
    def test_3(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        with check, allure.step("C58597: Check sponsors page heading title"):
            assert sponsors_page_obj.get_heading_title_text().strip() == TestSponsorsPage.sponsors_page_content["heading_title"].strip()
        with check, allure.step("C58597: Check sponsors page heading description"):
            assert sponsors_page_obj.get_heading_description_text() == TestSponsorsPage.sponsors_page_content["heading_description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Sponsors card section appearance")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58565", "C58565")
    @allure.testcase("58564", "C58564")
    @allure.testcase("58566", "C58566")
    @pytest.mark.dependency(depends=["test_1"])
    def test_4(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        expected_cards = TestSponsorsPage.sponsors_page_content["logos"]
        with check, allure.step("C58565: Check sponsors cards number"):
            assert sponsors_page_obj.get_sponsor_cards_number() == len(expected_cards)
        with check, allure.step("C58564: Check are sponsors cards images"):
            assert sponsors_page_obj.sponsor_cards_are_images()
        i = 0
        for image in expected_cards:
            with check, allure.step(f"C58566: {image} image is correct"):
                assert sponsors_page_obj.get_sponsors_card_image(i) == image
            i = i + 1

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Get Involved section appearance")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58567", "C58567")
    @pytest.mark.dependency(depends=["test_1"])
    def test_5(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        sponsors_page_obj.scroll_to_benefits_section(TestSponsorsPage.current_browser)
        with check, allure.step("C58567: Gen involved title is visible"):
            assert sponsors_page_obj.is_get_involved_title_visible()
        with check, allure.step("C58567: Gen involved description is visible"):
            assert sponsors_page_obj.is_get_involved_description_visible()
        if TestSponsorsPage.sponsors_page_content["benefits_link_text"] != "":
            with check, allure.step("C58567: Gen involved button is visible"):
                assert sponsors_page_obj.is_get_involved_button_visible()
        with check, allure.step("C58567: Benefits section is visible"):
            assert sponsors_page_obj.is_benefits_section_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Check get Involved title")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58568", "C58568")
    @pytest.mark.dependency(depends=["test_1"])
    def test_6(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        with check, allure.step("C58568: Gen involved title is correct"):
            expected_title = TestSponsorsPage.sponsors_page_content["benefits_title"].strip()
            assert expected_title == sponsors_page_obj.get_get_involved_title_text().strip()

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Check get Involved description")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58569", "C58569")
    @pytest.mark.dependency(depends=["test_1"])
    def test_7(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        with check, allure.step("C58569: Gen involved description is correct"):
            expected_description = TestSponsorsPage.sponsors_page_content["benefits_description"]
            assert expected_description == sponsors_page_obj.get_get_involved_description_text()

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Benefits banner appearance")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58570", "C58570")
    @pytest.mark.dependency(depends=["test_1"])
    def test_8(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        with check, allure.step("C58570: Benefits titles are visible"):
            assert sponsors_page_obj.are_benefits_titles_visible()
        with check, allure.step("C58570: Benefits descriptions are visible"):
            assert sponsors_page_obj.are_benefits_descriptions_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Benefits banners number")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58571", "C58571")
    @pytest.mark.dependency(depends=["test_1"])
    def test_9(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        with check, allure.step("C58571: Check benefits elements number"):
            expected_number = len(TestSponsorsPage.sponsors_page_content["themes_titles"])
            assert expected_number == sponsors_page_obj.get_benefits_elements_number()

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Benefits banners titles and descriptions")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58572", "C58572")
    @allure.testcase("58573", "C58573")
    @pytest.mark.dependency(depends=["test_1"])
    def test_10(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        benefits_number = len(TestSponsorsPage.sponsors_page_content["themes_titles"])
        actual_titles = sponsors_page_obj.get_benefits_title_text()
        actual_descriptions = sponsors_page_obj.get_benefits_description_text()
        for i in range(benefits_number):
            with check, allure.step(f"C58572: '{actual_titles[i]}' title is correct"):
                assert actual_titles[i] == TestSponsorsPage.sponsors_page_content["themes_titles"][i]
            with check, allure.step(f"C58573: '{actual_titles[i]}' description is correct"):
                assert actual_descriptions[i] == TestSponsorsPage.sponsors_page_content["themes_descriptions"][i]

    @severity(severity_level.NORMAL)
    @allure.feature('Sponsors page')
    @allure.title("Get in touch button")
    @allure.issue("QP-270", "Story QP-270")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58582", "C58582")
    @pytest.mark.dependency(depends=["test_1"])
    def test_11(self, driver):
        sponsors_page_obj = SponsorsPage(driver)
        main_nav_obj = MainNavigation(driver)
        with check, allure.step("C58582: Check button text"):
            expected_text = TestSponsorsPage.sponsors_page_content["benefits_link_text"]
            assert expected_text == sponsors_page_obj.get_get_involved_button_text()
        with check, allure.step("C58582: Click get in touch button"):
            sponsors_page_obj.click_get_involved_button()
            main_nav_obj.wait_page_to_load()
            expected_url = BaseClass.url[:-1] + TestSponsorsPage.sponsors_page_content["benefits_link_url"]
            assert driver.current_url == expected_url
        main_nav_obj.click_sponsors_button()
        main_nav_obj.wait_page_to_load()
