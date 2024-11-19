import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
EMAIL = os.getenv("EMAIL")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
KCURL = os.getenv("KCURL")
API_URL = os.getenv("APIURL")
CMS_URL = os.getenv("CMS_URL")
CMS_EMAIL = os.getenv("CMS_EMAIL")
CMS_PASSWORD = os.getenv("CMS_PASSWORD")
