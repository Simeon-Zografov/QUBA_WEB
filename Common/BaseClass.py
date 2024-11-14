import os
import shutil
import subprocess
import time
import socket
from base64 import b64encode

import pytest
from dotenv import load_dotenv
from selenium.webdriver import Proxy
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.proxy import ProxyType
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
                # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
                geco_driver_path = os.path.join(project_folder, 'Resources', 'geckodriver')
                serv = FirefoxService(geco_driver_path)
                driver = webdriver.Firefox(service=serv)
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
        project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        mitmdump_path = shutil.which("mitmdump")
        script_path = os.path.join(project_folder, "Common", "ResponseInterception.py")

        # def test_port_open(used_port):
        #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #         s.settimeout(1)
        #         try:
        #             s.bind(("127.0.0.1", used_port))
        #             print(f"Port {used_port} is available.")
        #         except Exception as e:
        #             print(f"Failed to bind to port {used_port}: {e}")

        if mitmdump_path is None:
            raise FileNotFoundError("mitmdump executable not found in PATH. Please ensure mitmproxy is installed.")
        if browser == "chrome":
            port = "8082"
        elif browser == "edge":
            port = "9090"
        elif browser == "firefox":
            port = "9092"
        else:
            port = "8081"
        # port = "8082"
        #
        # test_port_open(int(port))

        mitmdump_process = subprocess.Popen([mitmdump_path, "-s", script_path, "--listen-port", port,
                                             "--set", f"test_name={test_name}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5)
        if mitmdump_process:
            print("Proxy subprocess started")
        if os.getenv('CI') == 'true':
            if browser == "chrome":
                options = ChromeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')
                chrome_driver_path = "/usr/bin/chromedriver"
                serv = ChromeService(chrome_driver_path)
                proxy_driver = webdriver.Chrome(service=serv, options=options)
            elif browser == "edge":
                options = EdgeOptions()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-infobars")
                options.add_argument(f'--proxy-server=https://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')
                serv = EdgeService(EdgeChromiumDriverManager().install())
                proxy_driver = webdriver.Edge(service=serv, options=options)
                print("Edge Proxy driver created")
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                geckodriver_driver_path = "/usr/bin/geckodriver"
                serv = FirefoxService(geckodriver_driver_path)
                proxy = f'127.0.0.1:{port}'
                webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": proxy,
                    "sslProxy": proxy,
                    "proxyType": "manual"}
                proxy_driver = webdriver.Firefox(service=serv, options=options)
            else:
                pytest.skip("Unsupported on the browser")
        else:
            if browser == "chrome":
                chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
                options = webdriver.ChromeOptions()
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')  # mitmproxy default proxy
                options.add_argument('--ignore-certificate-errors')  # Bypass cert errors if needed for testing

                serv = ChromeService(chrome_driver_path)
                proxy_driver = webdriver.Chrome(service=serv, options=options)
            elif browser == "edge":
                options = webdriver.EdgeOptions()
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')  # mitmproxy default proxy
                options.add_argument('--ignore-certificate-errors')  # Bypass cert errors if needed for testing

                proxy_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
            elif browser == "firefox":
                proxy = f'127.0.0.1:{port}'
                webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                    "httpProxy": proxy,
                    "sslProxy": proxy,
                    "proxyType": "manual"}

                geco_driver_path = os.path.join(project_folder, 'Resources', 'geckodriver')
                serv = FirefoxService(geco_driver_path)
                proxy_driver = webdriver.Firefox(service=serv)
            else:
                pytest.skip("Unsupported on the browser")
        proxy_driver.implicitly_wait(10)
        proxy_driver.maximize_window()
        yield proxy_driver
        proxy_driver.quit()
        mitmdump_process.terminate()
        mitmdump_process.wait()
