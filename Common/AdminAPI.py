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

    def get_about_page_content(self):
        url = BaseClass.cms_url.replace("/admin", "") + "/content-manager/single-types/api::about-page.about-page/?locale=en"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            content = {}
            themes_elements = {}
            images = []
            faq_elements = {}
            content["heading_title"] = response_data["heading"]["title"]
            content["heading_description"] = response_data["heading"]["description"]
            content["themes_title"] = response_data["themes"]["sectionTitle"]["title"]
            content["themes_description"] = response_data["themes"]["sectionTitle"]["description"]
            for theme in response_data["themes"]["themes"]:
                description = ""
                for paragraph in theme["description"]:
                    for child in paragraph["children"]:
                        description = description + child["text"].replace("\n", "").strip()
                description = str(re.sub(' +', ' ', description))
                themes_elements[theme["title"]] = description
            content["theme_elements"] = themes_elements
            content["gallery_title"] = response_data["imageGallery"]["sectionTitle"]["title"]
            content["gallery_description"] = response_data["imageGallery"]["sectionTitle"]["description"]
            for image in response_data["imageGallery"]["images"]:
                images.append(image["name"])
            content["gallery_images"] = images
            content["faq_title"] = response_data["faq"]["sectionTitle"]["title"]
            content["faq_description"] = response_data["faq"]["sectionTitle"]["description"]
            for faq in response_data["faq"]["FAQ"]:
                answer = ""
                for paragraph in faq["answer"]:
                    for child in paragraph["children"]:
                        answer = answer + child["text"].replace("\n", "").strip()
                faq_elements[faq["question"]] = answer
            content["faq_elements"] = faq_elements
            return content
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_home_page_content(self):
        url = BaseClass.cms_url.replace("/admin", "") + "/content-manager/single-types/api::home-page.home-page/?locale=en"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            content = {}
            description_text = ""
            download_stats = {}
            site_carousel_sites = {}
            content["hero_title"] = response_data["hero"]["title"]
            content["hero_subtitle"] = response_data["hero"]["subtitle"]
            content["hero_image"] = response_data["hero"]["coverImage"]["name"]
            content["hero_link_text"] = response_data["hero"]["link"]["text"]
            content["hero_link_url"] = response_data["hero"]["link"]["url"]
            content["download_title"] = response_data["download"]["title"]
            for description in response_data["download"]["description"]:
                for paragraph in description["children"]:
                    description_text = description_text + paragraph["text"].replace("\n", "").strip()
                description_text = str(re.sub(' +', ' ', description_text))
            content["download_description"] = description_text
            content["download_image"] = response_data["download"]["showcase"]["slides"][0]["name"]
            for stat in response_data["download"]["stats"]:
                format_value = f'{stat["value"]:,}'
                download_stats[format_value] = stat["description"]
            content["download_stats"] = download_stats
            content["site_carousel_title"] = response_data["siteCarousel"]["sectionTitle"]["title"]
            content["site_carousel_description"] = response_data["siteCarousel"]["sectionTitle"]["description"]
            content["site_carousel_link_text"] = response_data["siteCarousel"]["sectionTitle"]["linkText"]
            content["site_carousel_link_url"] = response_data["siteCarousel"]["sectionTitle"]["linkUrl"]
            i = 0
            for site in response_data["siteCarousel"]["sites"]:
                site_carousel_sites[i] = site["title"]
                i = i + 1
            content["site_carousel_sites"] = site_carousel_sites
            content["event_carousel_title"] = response_data["eventCarousel"]["sectionTitle"]["title"]
            content["event_carousel_description"] = response_data["eventCarousel"]["sectionTitle"]["description"]
            content["event_carousel_link_text"] = response_data["eventCarousel"]["sectionTitle"]["linkText"]
            content["event_carousel_link_url"] = response_data["eventCarousel"]["sectionTitle"]["linkUrl"]
            return content
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None
