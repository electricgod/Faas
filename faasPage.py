import json
import time
import datetime
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/temp/naas.log',
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class FaasPage():

    global pageIds
    with open('../data/faasPage.json') as faas_page_id_file:
          pageIds = json.load(faas_page_id_file)

    def __init__(self, driver):
        self.driver = driver
    def verifyPageTitle(self):
        time.sleep(2)
        assert self.driver.title == 'Automazione | Charter Communications'
        logging.info('FaaS page title has been verified...')

    # Search through the Faas functions
    def searchFunctionList(self):
        try:
            if self.driver != None:

                time.sleep(5)
                logging.info('Start Faas function search field tests from the Execute tab')
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).click()
                time.sleep(2)
                # Find any function with k-d: positive test
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).send_keys('k-d')
                logging.info('Faas functions with k-d are searched and found...')
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).clear()
                time.sleep(2)
                # Find any function with ka-p: negative test
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).send_keys('ka-p')
                logging.info('Faas functions with ka-p are searched and NOT found...')
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).send_keys("cli-command")
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['faasFunctionSearchedExec']).click()
                logging.info('Faas function cli-command is searched, found and selected...')
                logging.info('End Faas function search field tests')
                time.sleep(5)
            else:
                logging.warning('Web driver issue is found')

        except NoSuchElementException:
            fileName = '../reports/screenshot-testFaas-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error('Element Exception in faasPage - searchFunctionList() func. Screenshot is taken and saved in reports folder.')
            raise

    # Fill the function form fields
    def fillFunctionForm(self, functionName, userID, userName, firstDevice, secondDevice):
        try:
            if self.driver != None:
                # Select the Function section
                time.sleep(10)
                logging.info('%s execution tests...', functionName)
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).click()
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['searchFunctions']).send_keys(functionName)
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['faasFunctionSearchedExec']).click()
                logging.info('%s is searched, found and selected...', functionName)
                time.sleep(4)
                # Fill in the function fields
                self.driver.find_element_by_xpath(pageIds['functionInput1']).send_keys(userID)
                logging.info('First field is populated...')
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['functionInput2']).send_keys(userName)
                logging.info('Second field is populated...')
                time.sleep(2)
                # Select devices section: break this out into a new function
                self.driver.find_element_by_xpath(pageIds['selectDevicesExpand']).click()
                logging.info('Device list is expanded. Waiting for Device list load to complete...')
                time.sleep(15)  # The Device List does not always load quickly adjust as needed
                # Odd behavior with the data-qa-ids in the device list. This is fixed by going to the Selected tab and then back to Available tab.
                self.driver.find_element_by_xpath(pageIds['devicesAvailableTab']).click()
                logging.info('Device list Available tab is selected...')
                self.driver.find_element_by_xpath(pageIds['searchDevices']).clear()
                logging.info('Device search field is cleared...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['searchDevices']).send_keys(firstDevice)
                logging.info('Device search field is populated with the first device...')
                self.driver.find_element_by_xpath(pageIds['devicesFilteredAddButton']).click()
                logging.info('Device is added via Select All Filtered button...')
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['devicesSelectedTab']).click()
                logging.info('Selected tab is now displaying 1 device...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['devicesAvailableTab']).click()
                logging.info('Available devices tab is displayed...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['searchDevices']).clear()
                logging.info('Device search field is cleared...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['searchDevices']).send_keys(secondDevice)
                logging.info('Device search field is populated...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['devicesFilteredAddButton']).click()
                logging.info('Device is added via Select All Filtered button...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['devicesSelectedTab']).click()
                logging.info('Selected tab is now displaying 2 devices...')
                # time.sleep(10)
                # self.driver.find_element_by_xpath(pageIds['functionExecuteButton']).click()
                # logging.info('%s is executed...', userFaaS)
                time.sleep(5)
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testFaasCLI-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error('Element Exception in faasPage - fillFunctionForm() func. Screenshot is taken and saved in reports folder.')
            raise

    # Device list add devices
    def deviceList(self, firstDevice, secondDevice):
        try:
            if self.driver != None:
                time.sleep(2)
                logging.info('%s selecting from the device list...', firstDevice, secondDevice)
                self.driver.find_element_by_xpath(pageIds['selectDevicesExpand']).click()
                logging.info('Device list is expanded. Waiting for Device list load to complete...')
                time.sleep(15)  # The Device List does not always load quickly adjust as needed
                # Odd behavior with the data-qa-ids in the device list. This is fixed by going to the Selected tab and then back to Available tab.
                self.driver.find_element_by_xpath(pageIds['devicesAvailableTab']).click()
                logging.info('Device list Available tab is selected...')
                self.driver.find_element_by_xpath(pageIds['searchDevices']).clear()
                logging.info('Device search field is cleared...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['searchDevices']).send_keys(firstDevice)
                logging.info('%s is entered in the search field for the first device...', firstDevice)
                self.driver.find_element_by_xpath(pageIds['devicesFilteredAddButton']).click()
                logging.info('Device is added via Select All Filtered button...')
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['devicesSelectedTab']).click()
                logging.info('Selected tab is now displaying 1 device...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['devicesAvailableTab']).click()
                logging.info('Available devices tab is displayed...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['searchDevices']).clear()
                logging.info('Device search field is cleared...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['searchDevices']).send_keys(secondDevice)
                logging.info('%s is entered in the search field for the second device...', secondDevice)
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['devicesFilteredAddButton']).click()
                logging.info('Device is added via Select All Filtered button...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['devicesSelectedTab']).click()
                logging.info('Selected tab is now displaying 2 devices...')
                time.sleep(10)
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error(
                'Element Exception on faasPage - deviceList() func. Screenshot is taken and saved in reports folder.')
            raise

        # Device list functional tests
        def deviceListFunctionalTest(self, firstDevice, secondDevice):
            try:
                if self.driver != None:
                    time.sleep(2)
                    logging.info('%s selecting from the device list...', firstDevice, secondDevice)
                    self.driver.find_element_by_xpath(pageIds['selectDevicesExpand']).click()
                    logging.info('Device list is expanded. Waiting for Device list load to complete...')
                    time.sleep(15)  # The Device List does not always load quickly adjust as needed
                    # Odd behavior with the data-qa-ids in the device list. This is fixed by going to the Selected tab and then back to Available tab.
                    self.driver.find_element_by_xpath(pageIds['devicesAvailableTab']).click()
                    logging.info('Device list Available tab is selected...')
                    self.driver.find_element_by_xpath(pageIds['searchDevices']).clear()
                    logging.info('Device search field is cleared...')
                    time.sleep(5)
                    self.driver.find_element_by_xpath(pageIds['searchDevices']).send_keys(firstDevice)
                    logging.info('%s is entered in the search field for the first device...', firstDevice)
                    self.driver.find_element_by_xpath(pageIds['devicesFilteredAddButton']).click()
                    logging.info('Device is added via Select All Filtered button...')
                    time.sleep(2)
                    self.driver.find_element_by_xpath(pageIds['devicesSelectedTab']).click()
                    logging.info('Selected tab is now displaying 1 device...')
                    time.sleep(5)
                    self.driver.find_element_by_xpath(pageIds['devicesAvailableTab']).click()
                    logging.info('Available devices tab is displayed...')
                    time.sleep(5)
                    self.driver.find_element_by_xpath(pageIds['searchDevices']).clear()
                    logging.info('Device search field is cleared...')
                    time.sleep(5)
                    self.driver.find_element_by_xpath(pageIds['searchDevices']).send_keys(secondDevice)
                    logging.info('%s is entered in the search field for the second device...', secondDevice)
                    time.sleep(5)
                    self.driver.find_element_by_xpath(pageIds['devicesFilteredAddButton']).click()
                    logging.info('Device is added via Select All Filtered button...')
                    time.sleep(5)
                    self.driver.find_element_by_xpath(pageIds['devicesSelectedTab']).click()
                    logging.info('Selected tab is now displaying 2 devices...')
                    time.sleep(10)
                else:
                    logging.warning('Web driver issue is found')
            except NoSuchElementException:
                fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                    "%Y-%m-%d %H:%M") + '.png'
                self.driver.get_screenshot_as_file(fileName)
                logging.error(
                    'Element Exception on faasPage - deviceListFunctionalTest() func. Screenshot is taken and saved in reports folder.')
                raise

    # Click the Execute button for a function.
    def functionExecute(self, functionName):
        try:
            if self.driver != None:
                logging.info('Click the Execute button...')
                self.driver.find_element_by_xpath(pageIds['functionExecuteButton']).click()
                logging.info('%s is executed...', functionName)
                time.sleep(5)
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error('Element Exception on faasPage - executionPrompts() func. Screenshot is taken and saved in reports folder.')
            raise

    # Function post execution prompts
    def executionPrompts(self):
        try:
            if self.driver != None:
                logging.info('Starting post function execution user prompt tests...')
                time.sleep(5)
                self.driver.find_element_by_xpath(pageIds['functionInputYesButton']).click()
                logging.info('Yes button is selected...')
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['functionInputYesButton']).click()
                logging.info('Yes button is selected...')
                time.sleep(2)
                logging.info('History tab  is selected...')
                time.sleep(5)
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error('Element Exception on faasPage - executionPrompts() func. Screenshot is taken and saved in reports folder.')
            raise

    # Refresh the history tab results and select the most recent
    def refreshHistory(self, times):
        try:
            if self.driver != None:
                logging.info('Starting History refresh test...')
                logging.info('Establishing execution time...')
                before = *[text()[contains(.,""//
                after = ")]]"
                now = datetime.now()
                logging.info('%s is the time now...', now)
                timeEvent = now.strftime("%I:%M:")
                identifier = before + "'" + timeEvent + "'" + after
                logging.info("%s is the execution search information...", identifier)
                logging.info('History is being refreshed while waiting for the function to complete...')
                for iterations in range(0, times):
                    self.driver.find_element_by_xpath(pageIds['refreshButton']).click()
                    time.sleep(5)
                    logging.info(iterations)
                logging.info('Refreshing History tab complete...')
                self.driver.find_element_by_xpath(identifier).click()
                logging.info('Latest execution history results have been selected...')
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error('Element Exception on faasPage - refreshHistory() func. Screenshot is taken and saved in reports folder.')
            raise

    # Search the device grid by IP
    def searchDeviceGridByIp(self, ip):
        try:
            if self.driver != None:
                time.sleep(5)  # Device grid load delay
                logging.info('Starting Device Grid tests...')
                logging.info('%s IP address is searched for...', ip)
                self.driver.find_element_by_xpath(pageIds['deviceGridIPAddressSearchField']).clear()
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['deviceGridIPAddressSearchField']).send_keys(ip)
                logging.info('%s device has been searched and found...', ip)
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['device1IP']).click()
                logging.info('Device is selected by its IP address field...')
                time.sleep(3)
                self.driver.find_element_by_xpath(pageIds['device1HostName']).click()
                logging.info('Device is selected by its Host Name field...')
                time.sleep(3)
                self.driver.find_element_by_xpath(pageIds['device1SwVer']).click()
                logging.info('Device is selected by its software version field...')
                time.sleep(2)
                logging.info('%s device results have been launched...', ip)
                logging.info('Device Grid tests complete...')
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error(
                'Element Exception on faasPage - searchHistoryByIp() func. Screenshot is taken and saved in reports folder.')
            raise

    # Confirm firmware version matches
    def verifyDeviceVersion(self, version):
        try:
            if self.driver != None:
                time.sleep(2)
                logging.info('%s device version check is launched...', version)
                displayedText = self.driver.find_element_by_xpath(pageIds['textDeviceID']).text
                time.sleep(2)
                assert (version in displayedText)
                logging.info('%s matches the retrieved device version...', version)
            else:
                logging.warning('Web driver issue is found')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testMop-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") + '.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error(
                'Element Exception on faasPage - verifyVersion() func. Screenshot is taken and saved in reports folder.')
            raise

    def logout(self):
        try:
            if self.driver != None:
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['menu']).click()
                time.sleep(2)
                self.driver.find_element_by_xpath(pageIds['logout']).click()
                logging.info('User ability to logout of FaaS module has been verified...')
            else:
                logging.warning('Web driver issue encountered...')
        except NoSuchElementException:
            fileName = '../reports/screenshot-testFaaS-' + datetime.datetime.now().now().strftime(
                "%Y-%m-%d %H:%M") +'.png'
            self.driver.get_screenshot_as_file(fileName)
            logging.error('Element Exception on FaaS page - logout() method. Screenshot taken..')