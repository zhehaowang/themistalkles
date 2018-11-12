
import pytest
import os
import textwrap
import json

from appium import webdriver
from helpers import take_screenhot_and_logcat, ANDROID_APP_PATH, EXECUTOR


class TestAndroidBasicInteractions():
    PACKAGE = 'com.instagram.android'
    MAIN_ACTIVITY = '.activity.MainTabActivity'

    @pytest.fixture(scope='function')
    def driver(self, request, device_logger):
        calling_request = request._pyfuncitem.name
        driver = webdriver.Remote(
            command_executor=EXECUTOR,
            desired_capabilities={
                'app': ANDROID_APP_PATH,
                'platformName': 'Android',
                'automationName': 'UIAutomator2',
                'platformVersion': os.getenv('ANDROID_PLATFORM_VERSION') or '9',
                'deviceName': os.getenv('ANDROID_DEVICE_VERSION') or 'Android',
                'appActivity': self.MAIN_ACTIVITY
            }
        )

        def fin():
            take_screenhot_and_logcat(driver, device_logger, calling_request)
            driver.quit()

        request.addfinalizer(fin)

        driver.implicitly_wait(10)
        return driver

    def test_open_instagram(self, driver):
        with open('../credentials/insta.json') as cred:
            content = json.loads(cred.read())
            acc_usrname = content['username']
            acc_pwd = content['password']

        driver.start_activity(self.PACKAGE, self.MAIN_ACTIVITY)

        driver.implicitly_wait(5)
        login_button = driver.find_element_by_id('log_in')
        login_button.click()

        driver.implicitly_wait(5)
        username = driver.find_element_by_id('login_username')
        username.send_keys(acc_usrname)

        password = driver.find_element_by_id('login_password')
        password.send_keys(acc_pwd)

        driver.implicitly_wait(5)
        next_button = driver.find_element_by_id('next_button')
        next_button.click()

        