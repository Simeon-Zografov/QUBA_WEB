import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class BaseClass:
    load_dotenv()
    url = os.getenv("URL")
    password = os.getenv("PASSWORD")
    browsers = os.getenv("BROWSERS")
    email = os.getenv("EMAIL")
    email_password = os.getenv("EMAIL_PASSWORD")
    browsers = browsers.split(", ")
    api_url = os.getenv("APIURL")
    kcurl = os.getenv("KCURL")
    client_secret = os.getenv("CLIENT_SECRET")

    @pytest.fixture(scope="class", autouse=True)
    def driver(self, request):
        browser = request.param

        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        is_ci = os.getenv('CI') == 'true'
        if is_ci:
            if browser == "edge":
                # Set up Edge options
                options = EdgeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                serv = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=serv, options=options)
            else:
                options = ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                '''chrome_driver_path = "/usr/local/share/chrome_driver/chromedriver"
                serv = ChromeService(executable_path=chrome_driver_path)
                driver = webdriver.Chrome(service=serv, options=options)'''
                chrome_driver_path = "/usr/bin/chromedriver"
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv, options=options)
        else:
            if browser == "Edge":
                # edge_driver_path = os.path.join(project_folder, 'Resources', 'msedgedriver')
                # serv = EdgeService(edge_driver_path)
                # driver = webdriver.Edge(service=serv)
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            elif browser == "Chrome":
                chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv)
                # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            else:
                # firefox_driver_path = os.path.join(project_folder, 'Resources', 'geckodriver')
                # serv = FirefoxService(firefox_driver_path)
                # driver = webdriver.Firefox(service=serv)
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()
