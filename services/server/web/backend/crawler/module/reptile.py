from bs4 import BeautifulSoup
import requests
from requests.api import options
from selenium.webdriver import ChromeOptions, Chrome, Firefox, DesiredCapabilities
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import os
from msedge.selenium_tools import EdgeOptions, Edge
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()


class RequestAnalysisData():
    """ 
        url: request base url
        mode: set True send post request, otherwise send get request
        cookies: add cookie to request, default is empty dictionary
        headers: add headers to request, example {'User-agent': 'Mozilla/5.0'}
    """
    def __init__(self, **params):
        self.__url = params['url']
        self.__mode = params['mode']
        self.__cookies = params.get('cookies', {})
        self.__headers = params.get('headers', {})
        self.__response = self.__request_mode()
        self.__soup = BeautifulSoup(self.__response.text, 'html.parser')

    def __request_mode(self):
        if self.__mode is True:
            return requests.post(url=self.__url, verify=False, cookies=self.__cookies, headers=self.__headers)
        return requests.get(url=self.__url, verify=False, cookies=self.__cookies, headers=self.__headers)

    def __enter__(self):
        return self.__soup

    def __exit__(self, type, value, traceback):
        pass

class RequestPageSource():
    def __init__(self, **params):
        self.__url = params['url']
        self.__mode = params['mode']
        self.__cookies = params.get('cookies', {})
        self.__headers = params.get('headers', {})
        self.__response = self.__request_mode()

    def __request_mode(self):
        if self.__mode is True:
            return requests.post(url=self.__url, verify=False, cookies=self.__cookies, headers=self.__headers)
        return requests.get(url=self.__url, verify=False, cookies=self.__cookies, headers=self.__headers)

    def __enter__(self):
        return self.__response

    def __exit__(self, type, value, traceback):
        pass

class Automation():
    def __init__(self, webdriver_path=None, open_browser=False, browser_type='chrome'):
        self.__webdriver_path = webdriver_path
        self.__open_browser = open_browser
        self.__browser_type = browser_type.lower()

    def __check_driver_is_exists(self):
        return os.path.exists(self.__webdriver_path)

    def __generate_chrome_driver(self):
        self.__options = ChromeOptions()
        self.__options.binary_location = "/usr/bin/google-chrome"
        if self.__open_browser is False:
            self.__options.add_argument("--headless")
            self.__options.add_argument('--disable-software-rasterizer')
        # self.__options.add_argument('--disable-infobars')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument('--incognito')
        self.__options.add_argument('--disable-gpu')
        self.__options.add_argument('--disable-dev-shm-usage')
        # self.__options.add_argument('--lang=en-nz')
        # self.__options.add_argument('--lang=zh-tw')

        # self.__options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # self.__options.add_experimental_option('useAutomationExtension', False)
        # self.__options.add_experimental_option("prefs", {"profile.password_manager_enabled": False, "credentials_enable_service": False})

        # self.__options.add_argument('--disable-dev-shm-usage')
        self.__driver = Chrome(executable_path=self.__webdriver_path, chrome_options=self.__options)
        return self.__driver

    def __generate_edge_driver(self):
        # method 1 but not use option parameters in webdriver
        # self.__driver = webdriver.Edge(executable_path=self.__webdriver_path)
        # method 2 from msedge.selenium_tools import Edge and EdgeOptions
        self.__options = EdgeOptions()
        self.__options.use_chromium = True
        if self.__open_browser is False:
            self.__options.add_argument('--headless')
        self.__options.add_argument('--disable-gpu')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument('--disable-dev-shm-usage')
        
        self.__driver = Edge(executable_path=self.__webdriver_path, options=self.__options)
        return self.__driver

    def __generate_firefox_driver(self):
        self.__options = Options()
        if self.__open_browser is False:
            options.add_argument('--headless')
        self.__options.add_argument('--disable-gpu')
        self.__caps = DesiredCapabilities().FIREFOX
        self.__caps["marionette"] = True
        self.__driver = Firefox(executable_path=self.__webdriver_path, firefox_options=self.__options, capabilities=self.__caps)
        return self.__driver

    def __enter__(self):
        if self.__webdriver_path is None or self.__check_driver_is_exists() is False:
            raise Exception("The driver path not found")
        if self.__browser_type == 'chrome':
            return self.__generate_chrome_driver()
        elif self.__browser_type == 'edge':
            return self.__generate_edge_driver()
        elif self.__browser_type == 'firefox':
            return self.__generate_firefox_driver()

    def __exit__(self, exc_type, exc_value, exc_info):
        self.__driver.quit()

class AnalysisData():
    def __init__(self, page_source, parser_method):
        self.__page_source = page_source
        self.__parser_method = parser_method

    def __generate(self):
        return BeautifulSoup(self.__page_source, self.__parser_method)

    def __enter__(self):
        return self.__generate()

    def __exit__(self, exc_type, exc_value, exc_info):
        pass
