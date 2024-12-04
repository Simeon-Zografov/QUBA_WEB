import os
import shutil
import subprocess
import time
from urllib.parse import urlparse

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from Common.APIRequests import APIRequests
from Common.AdminAPI import AdminAPI


class BaseClass:

    api_requests = APIRequests()
    admin = AdminAPI()

    load_dotenv()

    browsers = os.getenv("BROWSERS")
    browsers = browsers.split(", ")
    url = os.getenv("URL")
    current_browser = None

    @classmethod
    def initialize_data(cls):
        cls.site_list = cls.api_requests.get_sites_list()
        cls.event_list = cls.api_requests.get_events_list()
        cls.home_page_content = cls.admin.get_home_page_content()
        cls.about_page_content = cls.admin.get_about_page_content()
        cls.sponsors_page_content = cls.admin.get_sponsors_page_content()
        cls.sites_page_content = cls.admin.get_sites_page_content()
        cls.contact_page_content = cls.admin.get_contact_page_content()
        cls.events_page_content = cls.admin.get_events_page_content()

    @pytest.fixture(scope="class", autouse=True)
    def driver(self, request):
        browser = request.param
        BaseClass.current_browser = browser
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
                chrome_driver_path = "/usr/bin/chromedriver"
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv, options=options)
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                options.set_preference("browser.cache.disk.enable", False)
                options.set_preference("network.proxy.type", 0)
                geckodriver_driver_path = "/usr/bin/geckodriver"
                serv = FirefoxService(geckodriver_driver_path)
                # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {"proxyType": "direct"}
                driver = webdriver.Firefox(service=serv, options=options)
            else:
                options = SafariOptions()
                options.page_load_strategy = 'eager'
                driver = webdriver.Safari(options=options)
        else:
            if browser == "edge":
                driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
                download_dir = os.path.join(project_folder, 'Resources', 'edge_download_dir')
                params = {
                    "behavior": "allow",
                    "downloadPath": download_dir
                }
                driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
            elif browser == "chrome":
                chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
                serv = ChromeService(chrome_driver_path)
                driver = webdriver.Chrome(service=serv)
                download_dir = os.path.join(project_folder, 'Resources', 'chrome_download_dir')
                params = {
                    "behavior": "allow",
                    "downloadPath": download_dir
                }
                driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
            elif browser == "firefox":
                options = FirefoxOptions()
                download_dir = os.path.join(project_folder, 'Resources', 'firefox_download_dir')
                options.set_preference("browser.cache.disk.enable", False)
                options.set_preference("network.proxy.type", 0)
                options.set_preference("browser.download.folderList", 2)
                options.set_preference("browser.download.dir", download_dir)
                options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/calendar")  # MIME type for .ics
                options.set_preference("browser.download.manager.showWhenStarting", False)

                geco_driver_path = os.path.join(project_folder, 'Resources', 'geckodriver')
                serv = FirefoxService(geco_driver_path)
                driver = webdriver.Firefox(service=serv, options=options)
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

        mitmdump_process = subprocess.Popen([mitmdump_path, "-s", script_path, "--listen-port", port,
                                             "--set", f"test_name={test_name}"], stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL)  #
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
                options.add_argument("--allow-insecure-localhost")
                options.add_argument("--disable-http2")
                serv = EdgeService(EdgeChromiumDriverManager().install())
                proxy_driver = webdriver.Edge(service=serv, options=options)
            elif browser == "firefox":
                options = FirefoxOptions()
                options.add_argument("--headless")
                options.set_preference("network.proxy.type", 1)  # 1 = Manual proxy configuration
                options.set_preference("network.proxy.http", "127.0.0.1")
                options.set_preference("network.proxy.http_port", int(port))
                options.set_preference("network.proxy.ssl", "127.0.0.1")
                options.set_preference("network.proxy.ssl_port", int(port))
                options.set_preference("network.proxy.share_proxy_settings", True)
                options.set_preference("network.proxy.no_proxies_on", "")  # Disable bypassing proxy
                options.set_preference("network.proxy.allow_hijacking_localhost", True)  # Allow localhost interception
                options.set_preference("dom.security.https_only_mode", False)  # Avoid HTTPS-only mode issues
                options.set_preference("browser.cache.disk.enable", False)  # Disable caching to avoid stale data
                options.set_preference("network.dns.disableIPv6", True)
                options.set_preference("devtools.console.stdout.content", True)
                geckodriver_driver_path = "/usr/bin/geckodriver"
                serv = FirefoxService(geckodriver_driver_path)
                # proxy = f'127.0.0.1:{port}'
                # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                #     "httpProxy": proxy,
                #     "sslProxy": proxy,
                #     "proxyType": "manual"}
                proxy_driver = webdriver.Firefox(service=serv, options=options)
            else:
                pytest.skip("Mitmproxy unsupported on the browser")
        else:
            if browser == "chrome":
                chrome_driver_path = os.path.join(project_folder, 'Resources', 'chromedriver')
                options = webdriver.ChromeOptions()
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')

                serv = ChromeService(chrome_driver_path)
                proxy_driver = webdriver.Chrome(service=serv, options=options)
            elif browser == "edge":
                options = webdriver.EdgeOptions()
                options.add_argument(f'--proxy-server=http://127.0.0.1:{port}')
                options.add_argument('--ignore-certificate-errors')

                proxy_driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()),
                                              options=options)
            elif browser == "firefox":
                options = FirefoxOptions()
                # proxy = f'127.0.0.1:{port}'
                # webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
                #     "httpProxy": proxy,
                #     "sslProxy": proxy,
                #     "proxyType": "manual"}
                options.set_preference("network.proxy.type", 1)  # 1 = Manual proxy configuration
                options.set_preference("network.proxy.http", "127.0.0.1")
                options.set_preference("network.proxy.http_port", int(port))
                options.set_preference("network.proxy.ssl", "127.0.0.1")
                options.set_preference("network.proxy.ssl_port", int(port))
                options.set_preference("network.proxy.share_proxy_settings", True)
                options.set_preference("network.proxy.no_proxies_on", "")  # Disable bypassing proxy
                options.set_preference("network.proxy.allow_hijacking_localhost", True)  # Allow localhost interception
                options.set_preference("devtools.console.stdout.content", True)
                geco_driver_path = os.path.join(project_folder, 'Resources', 'geckodriver')
                serv = FirefoxService(geco_driver_path)
                proxy_driver = webdriver.Firefox(service=serv, options=options)
            else:
                pytest.skip("Mitmproxy unsupported on the browser")
        proxy_driver.implicitly_wait(10)
        proxy_driver.maximize_window()
        yield proxy_driver
        proxy_driver.quit()
        mitmdump_process.terminate()
        mitmdump_process.wait(timeout=10)
        time.sleep(5)
        if mitmdump_process:
            print("Mitmproxy process did not terminate in time. Forcing termination...")
            mitmdump_process.kill()
            time.sleep(5)

    @staticmethod
    def create_download_dir(browser):
        if browser != "safari":
            project_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            download_dir = os.path.join(project_folder, "Resources",  f"{browser}_download_dir")
            os.makedirs(download_dir, exist_ok=True)
            return download_dir
        else:
            default_dir = os.path.expanduser("~/Downloads")
            return default_dir

    @staticmethod
    def get_download_file_name(url):
        parsed_url = urlparse(url)
        file_name = os.path.basename(parsed_url.path)
        return f"{file_name}.ics"

    @staticmethod
    def cleanup_downloads(browser_name, download_dir, file_name):
        if browser_name.lower() == "safari":
            file_path = os.path.join(os.path.expanduser("~/Downloads"), file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            else:
                print(f"File not found: {file_path}")
        else:
            if os.path.exists(download_dir):
                shutil.rmtree(download_dir)
                print(f"Deleted directory: {download_dir}")
            else:
                print(f"Directory not found: {download_dir}")

    @classmethod
    def scroll_to_element(cls, driver, element, browser):
        location = element.location
        x = location['x']
        y = location['y']
        if browser == 'safari':
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            driver.execute_script(f"window.scrollTo({x}, {y - 150});")
        time.sleep(1)


BaseClass.initialize_data()
