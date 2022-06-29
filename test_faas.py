import json
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
from selenium import webdriver
import pytest
import sys, os
sys.path.insert(0, os.path.abspath('..'))
from pages.loginPage import LoginPage
from pages.landingPage import LandingPage
from pages.faasPage import FaasPage
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='../logs/main.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class TestFaas():

    @pytest.fixture()
    def setup(self):
        global dbData
        global deviceData
        global loginData
        global driver
        with open('../data/user.json') as data_file_login:
            loginData = json.load(data_file_login)
        with open('../data/device.json') as data_file_test_device:
            deviceData = json.load(data_file_test_device)
        global environment
        with open('../data/env.json') as data_file_env:
            envData = json.load(data_file_env)
        if envData['mode'] == '1' and envData['browser'] == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument('ignore-certificate-errors')
            driver = webdriver.Chrome("../drivers/chromedrivermac",chrome_options=options)
        elif envData['mode'] == '1' and envData['browser'] == 'firefox':
            driver = webdriver.Firefox()
            profile = webdriver.FirefoxProfile()
            profile.accept_untrusted_certs = True
        elif envData['mode'] == '1' and envData['browser'] == 'edge':
            cap = DesiredCapabilities().EDGE
            cap["platform"] = "ANY"
            driver = webdriver.Edge(executable_path='/usr/local/bin/msedgedriver', capabilities=cap)
        elif envData['mode'] == '1' and envData['browser'] == 'safari':
            driver = webdriver.Safari()
            driver.maximize_window()
        else:
            chrome_options = Options()
            chrome_options.add_argument('ignore-certificate-errors')
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--window-size=1920x1080")
            driver = webdriver.Chrome(options=chrome_options, executable_path="../drivers/chromedriverlinux")
            logging.info('Test configuration mode has been set to headless browser in env.json file!')
        driver.implicitly_wait(2)
        driver.maximize_window()
        driver.get(os.environ.get('URL'))
        logging.info('FaaS test started...')
        yield
        driver.quit()
        logging.info('FaaS test exited...')

    def test_faas(self,setup):

        loginPage = LoginPage(driver)
        loginPage.login(loginData['username1'], loginData['password1'])
        landingPage = LandingPage(driver)
        landingPage.goDarkTheme()
        landingPage.goFaas()
        faasPage = FaasPage(driver)
        faasPage.verifyPageTitle()

        # faasPage.searchFunctionList()
        faasPage.fillFunctionForm("device-ver-audit", "22222222", "RGK_test", "96.34.226.102", "96.34.226.131")
        # faasPage.deviceList("96.34.226.102", "96.34.226.131)
        faasPage.functionExecute("device-ver-audit")
        faasPage.executionPrompts()
        faasPage.refreshHistory(6)
        faasPage.searchDeviceGridByIp('96.34.226.131')
        faasPage.verifyDeviceVersion('Version 6.4.2')
        # faasPage.deviceListFunctionalTest()

        faasPage.logout()
