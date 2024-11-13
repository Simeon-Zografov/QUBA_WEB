import os
import shutil
import subprocess
import time

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
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
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
    cms_url = os.getenv("CMS_URL")
    cms_email = os.getenv("CMS_EMAIL")
    cms_password = os.getenv("CMS_PASSWORD")

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
            elif browser == "chrome":
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
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                geckodriver_driver_path = "/usr/bin/geckodriver"
                serv = FirefoxService(geckodriver_driver_path)
                driver = webdriver.Firefox(service=serv, options=options)
                # options.headless = True
                # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            else:
                options = SafariOptions()
                options.page_load_strategy = 'eager'
                driver = webdriver.Safari(options=options)
        else:
            if browser == "edge":
                # edge_driver_path = os.path.join(project_folder, 'Resources', 'msedgedriver')
                # serv = EdgeService(edge_driver_path)
                # driver = webdriver.Edge(service=serv)
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
            elif browser == "chrome":
                chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv)
                # driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
            elif browser == "firefox":
                # firefox_driver_path = os.path.join(project_folder, 'Resources', 'geckodriver')
                # serv = FirefoxService(firefox_driver_path)
                # driver = webdriver.Firefox(service=serv)
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
            else:
                options = SafariOptions()
                options.page_load_strategy = 'eager'
                driver = webdriver.Safari(options=options)

        driver.implicitly_wait(10)
        driver.maximize_window()
        yield driver
        driver.quit()

    @pytest.fixture(scope="function", autouse=False)
    def proxy_driver(self, request):
        browser = request.node.callspec.params["driver"]
        test_name = request.param
        print(browser)
        print(test_name)
        # browser = getattr(request, "param", None)
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mitmdump_path = shutil.which("mitmdump")
        script_path = os.path.join(project_folder, "Common", "ResponseInterception.py")
        print("Proxy fixture started")

        if mitmdump_path is None:
            raise FileNotFoundError("mitmdump executable not found in PATH. Please ensure mitmproxy is installed.")
        if browser == "chrome":
            port = "8082"
        elif browser == "edge":
            port = "8084"
        else:
            port = "8081"
        # port = "8082"
        mitmdump_process = subprocess.Popen([mitmdump_path, "-s", script_path, "--listen-port", port,
                                             "--set", f"test_name={test_name}"])
        print("Proxy subprocess started")
        if browser == "chrome":
            chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
            options = webdriver.ChromeOptions()
            options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')  # mitmproxy default proxy
            options.add_argument('--ignore-certificate-errors')  # Bypass cert errors if needed for testing

            serv = ChromeService(chrome_driver_path)
            proxy_driver = webdriver.Chrome(service=serv, options=options)
        else:
            options = webdriver.EdgeOptions()
            options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')  # mitmproxy default proxy
            options.add_argument('--ignore-certificate-errors')  # Bypass cert errors if needed for testing

            proxy_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
        # elif browser == "firefox":
        #     options = FirefoxOptions()
        #     # firefox_profile = webdriver.FirefoxProfile()
        #     # Specify to use manual proxy configuration.
        #     options.set_preference('network.proxy.type', 1)
        #     # Set the host/port.
        #     options.set_preference('network.proxy.http', 'http://127.0.0.1')
        #     options.set_preference('network.proxy.https_port', port)
        #     options.set_preference('network.proxy.ssl', 'http://127.0.0.1')
        #     options.set_preference('network.proxy.ssl_port', port)
        #     # options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
        #     # options.set_preference("security.enterprise_roots.enabled", True)
        #     # options.set_preference("network.proxy.allow_hijacking_localhost", True)
        #     # options.set_preference("devtools.console.stdout.content", True)
        #
        #     proxy_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
        # else:
        #     options = SafariOptions()
        #     options.page_load_strategy = 'eager'
        #     proxy_driver = webdriver.Safari(options=options)
        print("Proxy driver created")
        proxy_driver.implicitly_wait(10)
        proxy_driver.maximize_window()
        yield proxy_driver
        proxy_driver.quit()
        mitmdump_process.terminate()
        mitmdump_process.wait()
