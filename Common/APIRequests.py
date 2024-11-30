import re
import requests
from Common.config import EMAIL, PASSWORD, CLIENT_SECRET, KCURL, API_URL


class APIRequests:

    def __init__(self, browser=None):
        self.token = self.get_bearer_token(browser)

    @staticmethod
    def get_bearer_token(browser):
        if browser is not None:
            email = EMAIL.replace("@", "+" + browser + "@")
        else:
            email = EMAIL
        print(email)
        body = {
            "grant_type": "password",
            "username": email,
            "password": PASSWORD,
            "client_id": "clm",
            "client_secret": CLIENT_SECRET,
            "scope": "openid"
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(KCURL, data=body, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            bearer_token = response_data.get("access_token")
            return bearer_token
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_sites_list(self):
        url = f"{API_URL}/site"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            sites = {}
            for site in response_data:
                site_id = site["id"]
                site_title = site["attributes"]["title"]
                site_summary = site["attributes"]["summary"]
                site_type = site["attributes"]["type"]
                site_image = site["attributes"]["assets"][0]["url"]
                filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', site_image)
                if filename:
                    filename = filename.group(0)
                sites[site_id] = {"title": site_title, "summary": site_summary, "type": site_type, "image": filename}
            return sites
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_individual_site(self, site_id):
        url = f"{API_URL}/site/{site_id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            site = {}
            site_description = ""
            exhibits = {}
            images = []
            facilities = []
            site_id = response_data["id"]
            site_title = response_data["attributes"]["title"]
            site_summary = response_data["attributes"]["summary"]
            site_type = response_data["attributes"]["type"]
            site_address = response_data["attributes"]["address"]
            site_opening_hours = response_data["attributes"]["openingHours"]
            if response_data["attributes"]["description"] is not None:
                site_description = response_data["attributes"]["description"].replace("<p>", "").replace("</p>", "")
            if response_data["attributes"]["exhibits"] is not None:
                for exhibit in response_data["attributes"]["exhibits"]:
                    exhibit_id = exhibit["id"]
                    exhibit_title = exhibit["attributes"]["title"]
                    exhibit_summary = exhibit["attributes"]["summary"]
                    filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', exhibit["attributes"]["assets"][0]["url"])
                    if filename:
                        filename = filename.group(0)
                    exhibit_image = filename.replace("%20", " ")
                    exhibits[exhibit_id] = {"title": exhibit_title, "summary": exhibit_summary, "image": exhibit_image}
            for image in response_data["attributes"]["assets"]:
                filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', image["url"])
                if filename:
                    filename = filename.group(0)
                images.append(filename.replace("%20", " "))
            if response_data["attributes"]["facilities"] is not None:
                for facility in response_data["attributes"]["facilities"]:
                    facilities.append(facility["attributes"]["name"])
            lat = response_data["attributes"]["location"]["lat"]
            long = response_data["attributes"]["location"]["long"]
            site_location = str(lat) + "," + str(long)
            site[site_id] = {
                "title": site_title,
                "summary": site_summary,
                "type": site_type,
                "address": site_address,
                "opening_hours": site_opening_hours,
                "description": site_description,
                "exhibit": exhibits,
                "images": images,
                "facilities": facilities,
                "location": site_location
            }
            return site
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_events_list(self):
        url = f"{API_URL}/event"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            events = {}
            for event in response_data:
                event_id = event["id"]
                event_title = event["attributes"]["title"]
                event_summary = event["attributes"]["summary"]
                event_start = event["attributes"]["startAt"]
                event_end = event["attributes"]["endAt"]
                event_image = event["attributes"]["assets"][0]["url"]
                filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', event_image)
                if filename:
                    filename = filename.group(0)
                events[event_id] = {
                    "title": event_title,
                    "summary": event_summary,
                    "start": event_start,
                    "end": event_end,
                    "image": filename
                }
            return events
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_saved_sites_list(self):
        url = f"{API_URL}/site/saved"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            sites = {}
            for site in response_data:
                site_id = site["id"]
                site_title = site["attributes"]["title"]
                site_summary = site["attributes"]["summary"]
                site_type = site["attributes"]["type"]
                site_image = site["attributes"]["assets"][0]["url"]
                filename = re.search(r'([^/]+?\.[a-zA-Z0-9]+)(?=\);|$)', site_image)
                if filename:
                    filename = filename.group(0)
                sites[site_id] = {"title": site_title, "summary": site_summary, "type": site_type, "image": filename}
            return sites
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def unsave_site(self, site_id):
        url = f"{API_URL}/site/unsave"
        body = {
            "id": site_id
        }
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(url, data=body, headers=headers)
        if response.status_code == 204:
            print(f"Site {site_id} unsaved")
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)

    def save_site(self, site_id):
        url = f"{API_URL}/site/save"
        body = {
            "id": site_id
        }
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.post(url, data=body, headers=headers)
        if response.status_code == 204:
            print(f"Site {site_id} saved")
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
