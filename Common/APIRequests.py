import requests

from Common.BaseClass import BaseClass


class APIRequests:

    def __init__(self):
        self.token = self.get_bearer_token()

    @staticmethod
    def get_bearer_token():
        body = {
            "grant_type": "password",
            "username": BaseClass.email,
            "password": BaseClass.password,
            "client_id": "clm",
            "client_secret": BaseClass.client_secret,
            "scope": "openid"
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(BaseClass.kcurl, data=body, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            bearer_token = response_data.get("access_token")
            return bearer_token
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_sites_list(self):
        url = f"{BaseClass.api_url}/site"
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
                sites[site_id] = {"title": site_title, "summary": site_summary, "type": site_type}
            return sites
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None

    def get_individual_site(self, site_id):
        url = f"{BaseClass.api_url}/site/{site_id}"
        headers = {
            "Authorization": f"Bearer {self.token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            site = {}
            exhibits = {}
            site_id = response_data["id"]
            site_title = response_data["attributes"]["title"]
            site_summary = response_data["attributes"]["summary"]
            site_address = response_data["attributes"]["address"]
            site_opening_hours = response_data["attributes"]["openingHours"]
            site_description = response_data["attributes"]["description"]
            if response_data["attributes"]["exhibits"] is not None:
                for exhibit in response_data["attributes"]["exhibits"]:
                    exhibit_id = exhibit["id"]
                    exhibit_title = exhibit["attributes"]["title"]
                    exhibit_summary = exhibit["attributes"]["summary"]
                    exhibits[exhibit_id] = {"title": exhibit_title, "summary": exhibit_summary}
            site[site_id] = {"title": site_title, "summary": site_summary, "address": site_address,
                             "opening_hours": site_opening_hours, "description": site_description, "exhibit": exhibits}
            return site
        else:
            print("Request failed with status code:", response.status_code)
            print("Response content:", response.text)
            return None
