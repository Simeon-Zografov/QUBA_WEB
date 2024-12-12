import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Pages.AboutPage import AboutPage
from Pages.HomePage import HomePage
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestAboutPage(BaseClass):

    @severity(severity_level.CRITICAL)
    @allure.feature('About page')
    @allure.title("User is navigated to the About page")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58509", "C58509")
    def test_1(self, driver):
        main_nav_obj = MainNavigation(driver)
        about_page_obj = AboutPage(driver)
        driver.get(self.url)
        main_nav_obj.click_about_button()
        with check, allure.step("C58509: Check the page title"):
            assert about_page_obj.is_about_page_title_visible(self.about_page_content["heading_title"])

    @severity(severity_level.CRITICAL)
    @allure.feature('About page')
    @allure.title("About page appearance")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58512", "C58512")
    def test_2(self, driver):
        main_nav_obj = MainNavigation(driver)
        about_page_obj = AboutPage(driver)
        home_page_obj = HomePage(driver)
        with check, allure.step("C58512: Main navigation is visible"):
            assert main_nav_obj.is_nav_bar_visible()
        with check, allure.step("C58512: Page heading is visible"):
            assert about_page_obj.is_heading_visible()
        with check, allure.step("C58512: Themes section is visible"):
            assert about_page_obj.is_themes_section_visible()
        with check, allure.step("C58512: Image gallery is visible"):
            assert about_page_obj.is_image_gallery_visible()
        with check, allure.step("C58512: FAQ section is visible"):
            assert about_page_obj.is_faq_section_visible()
        with check, allure.step("C58512: Transport section is visible"):
            assert about_page_obj.is_transport_section_visible(self.current_browser)
        with check, allure.step("C58512: Page footer is visible"):
            assert home_page_obj.is_app_footer_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check heading title text")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58510", "C58510")
    def test_3(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58510: Heading title text"):
            assert about_page_obj.get_heading_title_text().strip() == self.about_page_content["heading_title"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check heading title description")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58511", "C58511")
    def test_4(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58511: Check Hero banner description"):
            assert about_page_obj.get_heading_description_text().strip() == self.about_page_content["heading_description"].strip()

    @severity(severity_level.CRITICAL)
    @allure.feature('About page')
    @allure.title("Themes section appearance")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58513", "C58513")
    def test_5(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58513: Section title is visible"):
            assert about_page_obj.is_themes_title_visible()
        with check, allure.step("C58513: Section description is visible"):
            assert about_page_obj.is_themes_description_visible()
        with check, allure.step("C58513: Section cards are visible"):
            assert about_page_obj.get_theme_cards_number() > 0

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check themes section title text")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58514", "C58514")
    def test_6(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58514: Section title text"):
            assert about_page_obj.get_themes_title_text().strip() == self.about_page_content[
                "themes_title"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check themes section description text")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58515", "C58515")
    def test_7(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58515: Section description text"):
            assert about_page_obj.get_themes_description_text().strip() == self.about_page_content[
                "themes_description"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check themes cards")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58516", "C58516")
    @allure.testcase("58518", "C58518")
    @allure.testcase("58519", "C58519")
    def test_8(self, driver):
        about_page_obj = AboutPage(driver)
        theme_cards = list(self.about_page_content["theme_elements"].keys())
        theme_cards_number = len(theme_cards)
        with check, allure.step("C58516: Theme cards number is correct"):
            assert about_page_obj.get_theme_cards_number() == theme_cards_number
        for i in range(theme_cards_number):
            with check, allure.step(f"C58518: {theme_cards[i]} title is correct"):
                expected_title = theme_cards[i].strip()
                actual_title = about_page_obj.get_theme_card_title(i).strip()
                assert actual_title == expected_title
            with check, allure.step(f"C58519: {theme_cards[i]} description is correct"):
                expected_description = self.about_page_content["theme_elements"][theme_cards[i]].strip()
                actual_description = about_page_obj.get_theme_card_description(i).strip()
                assert actual_description == expected_description

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Image gallery with only one image")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58522", "C58522")
    @pytest.mark.parametrize("proxy_driver", ["about_page_test_9"], indirect=True)
    def test_9(self, proxy_driver):
        proxy_driver.get(self.url + "about")
        main_nav_obj = MainNavigation(proxy_driver)
        about_page_obj = AboutPage(proxy_driver)
        main_nav_obj.wait_page_to_load()
        about_page_obj.scroll_to_image_gallery(self.current_browser)
        with check, allure.step("C58522: Next image button is not visible"):
            assert not about_page_obj.is_next_slide_button_visible()
        with check, allure.step("C58522: Scroll bar is not visible"):
            assert not about_page_obj.is_image_carousel_scroll_visible()
        with check, allure.step("C58522: Only one image is visible"):
            assert len(about_page_obj.get_images()) == 1
        with check, allure.step("C58522: The correct image is displayed"):
            assert about_page_obj.get_images()[0] == self.about_page_content["gallery_images"][0]

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Image gallery with more than one image")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58523", "C58523")
    @pytest.mark.dependency(name="test_10")
    def test_10(self, driver):
        if len(self.about_page_content["gallery_images"]) <= 1:
            pytest.skip("Less images are uploaded in the CMS than required")
        about_page_obj = AboutPage(driver)
        about_page_obj.scroll_to_image_gallery(self.current_browser)
        image_list = about_page_obj.get_images()
        i = 0
        for image in image_list:
            with check, allure.step(f"C58523: The image {image} is correct"):
                assert image == self.about_page_content["gallery_images"][i]
            i = i + 1
        with check, allure.step("C58523: Next image button is visible"):
            assert about_page_obj.is_next_slide_button_visible()
        with check, allure.step("C58523: Scroll bar is visible"):
            assert about_page_obj.is_image_carousel_scroll_visible()
        driver.refresh()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Scroll images with buttons")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58524", "C58524")
    @pytest.mark.dependency(depends=["test_10"])
    def test_11(self, driver):
        about_page_obj = AboutPage(driver)
        about_page_obj.scroll_to_image_gallery(self.current_browser)
        with check, allure.step("C58524: Initially next is visible and previous is not"):
            assert about_page_obj.is_next_slide_button_visible() and not about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58524: Carousel position is at the start"):
            assert about_page_obj.get_image_carousel_position() == "start"
        with check, allure.step("C58524: Next and previous buttons after clicking next"):
            about_page_obj.click_next_slide_button()
            assert about_page_obj.is_next_slide_button_visible() and about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58524: Carousel position is at the middle"):
            assert about_page_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58524: Next and previous buttons at the end of the carousel"):
            position = about_page_obj.get_image_carousel_position()
            while position != "end":
                about_page_obj.click_next_slide_button()
                position = about_page_obj.get_image_carousel_position()
            assert not about_page_obj.is_next_slide_button_visible() and about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58524: Carousel position is at the end"):
            assert about_page_obj.get_image_carousel_position() == "end"
        with check, allure.step("C58524: Next and previous buttons after clicking previous"):
            about_page_obj.click_previous_slide_button()
            assert about_page_obj.is_next_slide_button_visible() and about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58524: Carousel position is at the middle"):
            assert about_page_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58524: Next and previous buttons at the start of the carousel"):
            position = about_page_obj.get_image_carousel_position()
            while position != "start":
                about_page_obj.click_previous_slide_button()
                position = about_page_obj.get_image_carousel_position()
            assert about_page_obj.is_next_slide_button_visible() and not about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58524: Carousel position is at the start"):
            assert about_page_obj.get_image_carousel_position() == "start"

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Scroll trough images")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58525", "C58525")
    @pytest.mark.dependency(depends=["test_10"])
    def test_12(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58525: Initially next is visible and previous is not"):
            assert about_page_obj.is_next_slide_button_visible() and not about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58525: Carousel position is at the start"):
            assert about_page_obj.get_image_carousel_position() == "start"
        with check, allure.step("C58525: Next and previous buttons after scrolling"):
            about_page_obj.scroll_right_in_image_gallery()
            assert about_page_obj.is_next_slide_button_visible() and about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58525: Carousel position is at the middle"):
            assert about_page_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58525: Next and previous buttons at the end of the carousel"):
            position = about_page_obj.get_image_carousel_position()
            while position != "end":
                about_page_obj.scroll_right_in_image_gallery()
                position = about_page_obj.get_image_carousel_position()
            assert not about_page_obj.is_next_slide_button_visible() and about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58525: Carousel position is at the end"):
            assert about_page_obj.get_image_carousel_position() == "end"
        with check, allure.step("C58525: Next and previous buttons after scrolling left"):
            about_page_obj.scroll_left_in_image_gallery()
            assert about_page_obj.is_next_slide_button_visible() and about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58525: Carousel position is at the middle"):
            assert about_page_obj.get_image_carousel_position() == "middle"
        with check, allure.step("C58525: Next and previous buttons at the start of the carousel"):
            position = about_page_obj.get_image_carousel_position()
            while position != "start":
                about_page_obj.scroll_left_in_image_gallery()
                position = about_page_obj.get_image_carousel_position()
            assert about_page_obj.is_next_slide_button_visible() and not about_page_obj.is_previous_slide_button_visible()
        with check, allure.step("C58525: Carousel position is at the start"):
            assert about_page_obj.get_image_carousel_position() == "start"

    @severity(severity_level.CRITICAL)
    @allure.feature('About page')
    @allure.title("FAQ section appearance")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58529", "C58529")
    def test_13(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58529: Section title is visible"):
            assert about_page_obj.is_faq_title_visible()
        with check, allure.step("C58529: Section description is visible"):
            assert about_page_obj.is_faq_description_visible()
        with check, allure.step("C58529: FAQ elements are visible"):
            assert about_page_obj.are_faq_elements_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check FAQ section title text")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58530", "C58530")
    def test_14(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58530: Section title text"):
            assert about_page_obj.get_faq_title_text().strip() == self.about_page_content["faq_title"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check FAQ section description text")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58531", "C58531")
    def test_15(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58531: Section description text"):
            assert about_page_obj.get_faq_description_text().strip() == self.about_page_content[
                "faq_description"].strip()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Check FAQ elements")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58526", "C58526")
    @pytest.mark.dependency(name="test_16")
    def test_16(self, driver):
        about_page_obj = AboutPage(driver)
        faq_elements = list(self.about_page_content["faq_elements"].keys())
        faq_elements_number = len(faq_elements)
        with check, allure.step("C58526: Theme cards number is correct"):
            assert about_page_obj.get_faq_elements_number() == faq_elements_number
        for i in range(faq_elements_number):
            with check, allure.step(f"C58526: {faq_elements[i]} question is correct"):
                about_page_obj.click_faq_element(i, self.current_browser)
                expected_question = faq_elements[i].strip()
                actual_question = about_page_obj.get_faq_element_question(i).strip()
                assert actual_question == expected_question
            with check, allure.step(f"C58526: {faq_elements[i]} answer is correct"):
                expected_answer = self.about_page_content["faq_elements"][faq_elements[i]].strip()
                actual_answer = about_page_obj.get_faq_element_answer(i).strip()
                assert actual_answer == expected_answer

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Expand FAQ elements")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58528", "C58528")
    @pytest.mark.dependency(depends=["test_16"])
    def test_17(self, driver):
        about_page_obj = AboutPage(driver)
        for i in range(about_page_obj.get_faq_elements_number()):
            with check, allure.step(f"C58528: {about_page_obj.get_faq_element_question(i)} is collapsed"):
                about_page_obj.click_faq_element(i, self.current_browser)
                assert not about_page_obj.is_faq_element_expanded(i)

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Expand FAQ elements")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58527", "C58527")
    @pytest.mark.dependency(depends=["test_16"])
    def test_18(self, driver):
        about_page_obj = AboutPage(driver)
        for i in range(about_page_obj.get_faq_elements_number()):
            with check, allure.step(f"C58527: {about_page_obj.get_faq_element_question(i)} is expanded"):
                about_page_obj.click_faq_element(i, self.current_browser)
                assert about_page_obj.is_faq_element_expanded(i)

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Transport section appearance")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58532", "C58532")
    def test_19(self, driver):
        about_page_obj = AboutPage(driver)
        with check, allure.step("C58532: Public transport card is visible"):
            assert about_page_obj.is_public_transport_card_visible()
        with check, allure.step("C58532: Parking card is visible"):
            assert about_page_obj.is_parking_card_visible()
        with check, allure.step("C58532: Taxi card is visible"):
            assert about_page_obj.is_taxi_card_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Transport section card titles")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58534", "C58534")
    def test_20(self, driver):
        about_page_obj = AboutPage(driver)
        i = 0
        for title in about_page_obj.cards_titles:
            with check, allure.step(f"C58534: {title} is correct"):
                assert title == about_page_obj.get_transport_cards_title(i)
            i = i + 1

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Transport section card descriptions")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58535", "C58535")
    def test_21(self, driver):
        about_page_obj = AboutPage(driver)
        i = 0
        for description in about_page_obj.card_descriptions:
            with check, allure.step(f"C58535: {about_page_obj.get_transport_cards_title(i)} description is correct"):
                assert description == about_page_obj.get_transport_cards_description(i)
            i = i + 1

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Public transport card link")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58536", "C58536")
    def test_22(self, driver):
        about_page_obj = AboutPage(driver)
        main_nav_obj = MainNavigation(driver)
        about_page_obj.scroll_to_transport_section(self.current_browser)
        with check, allure.step("C58536: Click public transport link"):
            about_page_obj.click_public_transport_card_link()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == self.url + "about/public-transport"
        main_nav_obj.click_about_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Parking card link")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58537", "C58537")
    def test_23(self, driver):
        about_page_obj = AboutPage(driver)
        main_nav_obj = MainNavigation(driver)
        about_page_obj.scroll_to_transport_section(self.current_browser)
        with check, allure.step("C58537: Click parking link"):
            about_page_obj.click_parking_card_link()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == self.url + "about/parking"
        main_nav_obj.click_about_button()
        main_nav_obj.wait_page_to_load()

    @severity(severity_level.NORMAL)
    @allure.feature('About page')
    @allure.title("Taxi card link")
    @allure.issue("QP-266", "Story QP-266")
    @allure.issue("QP-356", "Epic QP-356")
    @allure.testcase("58538", "C58538")
    def test_24(self, driver):
        about_page_obj = AboutPage(driver)
        main_nav_obj = MainNavigation(driver)
        about_page_obj.scroll_to_transport_section(self.current_browser)
        with check, allure.step("C58538: Click taxi link"):
            about_page_obj.click_taxi_card_link()
            main_nav_obj.wait_page_to_load()
            assert driver.current_url == self.url + "about/taxis"
        main_nav_obj.click_about_button()
        main_nav_obj.wait_page_to_load()
