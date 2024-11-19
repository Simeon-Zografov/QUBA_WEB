import re
import requests
from Common.BaseClass import BaseClass


class AdminAPI:

    def __init__(self):
        self.token = self.get_bearer_token()

    @staticmethod
    def get_bearer_token():
        body = {
            "email": BaseClass.cms_email,
            "password": BaseClass.cms_password
        }
        url = BaseClass.cms_url + "/login"
        response = requests.post(url, data=body)
        if response.status_code == 200:
            response_data = response.json()
            bearer_token = response_data["data"].get("token")
            return bearer_token
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_sponsors_page_content(self):
        url = BaseClass.cms_url.replace("/admin", "") + "/content-manager/single-types/api::sponsors-page.sponsors-page/?locale=en"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            content = {}
            logos = []
            benefit_titles = []
            benefit_descriptions = []
            content["heading_title"] = response_data["heading"]["title"]
            content["heading_description"] = response_data["heading"]["description"].replace("\n", "").strip()
            for logo in response_data["logos"]:
                logos.append(logo["image"].get("name"))
            content["logos"] = logos
            content["benefits_title"] = response_data["benefits"]["sectionTitle"]["title"]
            content["benefits_description"] = response_data["benefits"]["sectionTitle"]["description"].replace("\n", "").strip()
            content["benefits_link_text"] = response_data["benefits"]["sectionTitle"]["linkText"]
            content["benefits_link_url"] = response_data["benefits"]["sectionTitle"]["linkUrl"]
            for benefit in response_data["benefits"]["themes"]:
                benefit_titles.append(benefit["title"])
                description = ""
                for paragraph in benefit["description"]:
                    for child in paragraph["children"]:
                        description = description + child["text"].replace("\n", "").strip()
                benefit_descriptions.append(description)
            content["themes_titles"] = benefit_titles
            content["themes_descriptions"] = benefit_descriptions
            return content
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None
