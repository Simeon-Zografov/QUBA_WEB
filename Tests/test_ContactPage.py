import time
import allure
import pytest
from pytest_check import check
from allure import severity, severity_level
from Common import Email
from Pages.ContactPage import ContactPage
from Pages.MainNavigation import MainNavigation
from Common.BaseClass import BaseClass


@pytest.mark.parametrize("driver", BaseClass.browsers, indirect=True)
@pytest.mark.flaky(reruns=3, reruns_delay=1)
class TestContactPage(BaseClass):

    @severity(severity_level.CRITICAL)
    @allure.feature('Contact page')
    @allure.title("User is navigated to the Contact page")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58594", "C58594")
    @pytest.mark.dependency(name="test_1")
    def test_1(self, driver):
        contact_obj = ContactPage(driver)
        main_nav_obj = MainNavigation(driver)
        driver.get(self.url)
        main_nav_obj.wait_page_to_load()
        main_nav_obj.click_contact_button()
        with check, allure.step("C58594: Check the page title"):
            assert contact_obj.is_contact_page_title_visible(self.contact_page_content["heading_title"])

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Welcome message appearance")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58452", "C58452")
    @pytest.mark.dependency(depends=["test_1"])
    def test_2(self, driver):
        contact_obj = ContactPage(driver)
        with check, allure.step("C58452: Welcome title is visible"):
            assert contact_obj.is_contact_page_title_visible(self.contact_page_content["heading_title"])
        with check, allure.step("C58452: Welcome description is visible"):
            assert contact_obj.is_heading_description_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Welcome message text")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58453", "C58453")
    @pytest.mark.dependency(depends=["test_1"])
    def test_3(self, driver):
        contact_obj = ContactPage(driver)
        with check, allure.step("C58453: Welcome title is correct"):
            assert contact_obj.get_contact_page_title_text() == self.contact_page_content["heading_title"]
        with check, allure.step("C58453: Welcome description is correct"):
            assert contact_obj.get_heading_description_text() == self.contact_page_content["heading_description"]

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Age appearance")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58606", "C58606")
    @pytest.mark.dependency(depends=["test_1"])
    def test_4(self, driver):
        contact_obj = ContactPage(driver)
        with check, allure.step("C58606: Message section is visible"):
            assert contact_obj.is_message_section_visible()
        with check, allure.step("C58606: Details section is visible"):
            assert contact_obj.is_details_section_visible()
        contact_obj.scroll_to_transport_section(self.current_browser)
        with check, allure.step("C58606: Transport section is visible"):
            assert contact_obj.is_transport_section_visible()
        with check, allure.step("C58606: Footer is visible"):
            assert contact_obj.is_footer_visible()

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Name field appearance")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58979", "C58979")
    @pytest.mark.dependency(depends=["test_1"])
    def test_5(self, driver):
        contact_obj = ContactPage(driver)
        contact_obj.scroll_to_message_section(self.current_browser)
        with check, allure.step("C58979: Name field is visible"):
            assert contact_obj.is_name_field_visible()
        with check, allure.step("C58979: Check name field placeholder"):
            assert contact_obj.get_name_field_placeholder() == contact_obj.name_field_placeholder

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Populated name field")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58978", "C58978")
    @pytest.mark.dependency(depends=["test_1"])
    def test_6(self, driver):
        contact_obj = ContactPage(driver)
        random_name = contact_obj.generate_random_name()
        contact_obj.set_name_field(random_name)
        with check, allure.step("C58978: Check name field value"):
            assert contact_obj.get_name_field_value() == random_name

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Email field appearance")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58981", "C58981")
    @pytest.mark.dependency(depends=["test_1"])
    def test_7(self, driver):
        contact_obj = ContactPage(driver)
        with check, allure.step("C58981: Email field is visible"):
            assert contact_obj.is_email_field_visible()
        with check, allure.step("C58981: Check email field placeholder"):
            assert contact_obj.get_email_field_placeholder() == contact_obj.email_field_placeholder

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Populated email field")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58980", "C58980")
    @pytest.mark.dependency(depends=["test_1"])
    def test_8(self, driver):
        contact_obj = ContactPage(driver)
        random_email = contact_obj.generate_random_email()
        random_email = random_email.replace("@", "")
        contact_obj.set_email_field(random_email)
        with check, allure.step("C58980: Check email field value"):
            assert contact_obj.get_email_field_value() == random_email

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Email field validation")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58982", "C58982")
    @pytest.mark.dependency(depends=["test_1"])
    def test_9(self, driver):
        contact_obj = ContactPage(driver)
        contact_obj.click_send_message_button()
        with check, allure.step("C58982: Error message is visible"):
            assert contact_obj.is_invalid_email_error_visible()
        with check, allure.step("C58982: Error message text"):
            assert contact_obj.get_invalid_email_error_text() == contact_obj.invalid_email_error_message

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Message field appearance")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58984", "C58984")
    @pytest.mark.dependency(depends=["test_1"])
    def test_10(self, driver):
        contact_obj = ContactPage(driver)
        with check, allure.step("C58984: Message field is visible"):
            assert contact_obj.is_message_field_visible()
        with check, allure.step("C58984: Check message field placeholder"):
            assert contact_obj.get_message_field_placeholder() == contact_obj.message_field_placeholder

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Populated message field")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58983", "C58983")
    @pytest.mark.dependency(depends=["test_1"])
    def test_11(self, driver):
        contact_obj = ContactPage(driver)
        random_message = contact_obj.generate_random_message()
        contact_obj.set_message_field(random_message)
        with check, allure.step("C58980: Check message field value"):
            assert contact_obj.get_message_field_value() == random_message

    @severity(severity_level.NORMAL)
    @allure.feature('Contact page')
    @allure.title("Secondary details")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @allure.testcase("58987", "C58987")
    @allure.testcase("58988", "C58988")
    @allure.testcase("58989", "C58989")
    @pytest.mark.dependency(depends=["test_1"])
    def test_12(self, driver):
        contact_obj = ContactPage(driver)
        for detail_title, detail_content in self.contact_page_content["details"].items():
            with check, allure.step(f"C58987: {detail_title} section is visible"):
                assert contact_obj.is_details_element_visible(detail_title)
            with check, allure.step(f"C58987: {detail_title} content is correct"):
                assert contact_obj.get_details_element_text(detail_title) == detail_content

    @severity(severity_level.CRITICAL)
    @allure.feature('Contact page')
    @allure.title("Successful message send")
    @allure.issue("QP-271", "QP-271")
    @allure.issue("QP-356", "QP-356")
    @pytest.mark.dependency(depends=["test_1"])
    def test_13(self, driver):
        contact_obj = ContactPage(driver)
        random_name = contact_obj.generate_random_name()
        random_email = self.current_browser + "_" + contact_obj.generate_random_email()
        random_message = contact_obj.generate_random_message()
        contact_obj.set_name_field(random_name)
        contact_obj.set_email_field(random_email)
        contact_obj.set_message_field(random_message)
        contact_obj.click_send_message_button()
        time.sleep(20)
        with check, allure.step("Success message is visible"):
            assert contact_obj.is_success_message_visible()
        expected_email = f"Full name: {random_name}\r\nEmail address: {random_email}\r\nYour message: {random_message}\r\n"
        actual_email = Email.get_latest_email_content(self.current_browser)
        with check, allure.step("Email is correct"):
            assert actual_email == expected_email
        driver.refresh()
