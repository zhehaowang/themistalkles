
import pytest
import os
import textwrap
import json
from datetime import datetime

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from helpers import take_screenhot_and_logcat, EXECUTOR, get_structured_feeds

class TestAndroidBasicInteractions():
    PACKAGE = 'com.instagram.android'
    MAIN_ACTIVITY = '.activity.MainTabActivity'
    WAIT_ACTIVITY = 'com.instagram.nux.activity.SignedOutFragmentActivity'

    HEART_XPATH = '//android.widget.FrameLayout[@content-desc="Activity"]'
    FOLLOWING_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[1]'

    @pytest.fixture(scope='function')
    def driver(self, request, device_logger):
        calling_request = request._pyfuncitem.name
        driver = webdriver.Remote(
            command_executor = EXECUTOR,
            desired_capabilities = {
              "platformName": "Android",
              "platformVersion": "9",
              "deviceName": "Android",
              "automationName": "UIAutomator2",
              "app": "/Users/zwang541/personal/themistalkles/bin/instagram-70-0-0-22-98.apk",
              "appWaitPackage": self.PACKAGE,
              "appWaitActivity": self.WAIT_ACTIVITY
            }
        )

        def fin():
            take_screenhot_and_logcat(driver, device_logger, calling_request)
            driver.quit()

        request.addfinalizer(fin)

        driver.implicitly_wait(10)
        return driver

    def test_open_instagram_and_print_feeds(self, driver):
        with open('../credentials/insta.json') as cred:
            content = json.loads(cred.read())
            acc_usrname = content['username']
            acc_pwd = content['password']

        driver.start_activity(
            self.PACKAGE,
            self.MAIN_ACTIVITY,
            app_wait_activity = self.WAIT_ACTIVITY)

        # log in
        wait = WebDriverWait(driver, 20)
        curr_wait = wait.until(EC.element_to_be_clickable((By.ID, 'log_in_button')))

        login_button = driver.find_element_by_id('log_in_button')
        login_button.click()

        curr_wait = wait.until(EC.element_to_be_clickable((By.ID, 'login_username')))
        username = driver.find_element_by_id('login_username')
        username.send_keys(acc_usrname)

        password = driver.find_element_by_id('password')
        password.send_keys(acc_pwd)

        next_button = driver.find_element_by_id('next_button')
        next_button.click()

        # go to 'following'
        curr_wait = wait.until(EC.element_to_be_clickable((By.XPATH, self.HEART_XPATH)))
        heart_icon = driver.find_element(By.XPATH, self.HEART_XPATH)
        heart_icon.click()

        curr_wait = wait.until(EC.element_to_be_clickable((By.ID, 'fixed_tabbar_tabs_container')))
        following_button = driver.find_element(By.XPATH, self.FOLLOWING_XPATH)
        following_button.click()

        driver.implicitly_wait(2)
        text_feeds = []

        def record_feeds(driver, text_feeds):
            text_elements = driver.find_elements(By.ID, 'row_newsfeed_text')
            for elem in text_elements:
                if not elem.text in text_feeds:
                    text_feeds.append(elem.text)
            # we only care about collecting the feed till 1d ago, assuming daily
            # run
            if len(text_feeds) > 0:
                last = text_feeds[-1].split()[-1]
                if not last.endswith('h'):
                    return False
            return True

        # record feeds in 'following'
        scroll_further = True
        while scroll_further:
            driver.swipe(470, 1400, 470, 950, 330)
            driver.implicitly_wait(1)
            scroll_further = record_feeds(driver, text_feeds)

        print(text_feeds)
        with open('text_feeds_' + str(datetime.now()) + '.log', 'w') as writefile:
            writefile.write(text_feeds)

        # process structured feeds
        structured_feeds = get_structured_feeds(text_feeds)
        with open('structured_feeds_' + str(datetime.now()) + '.log', 'w') as writefile:
            writefile.write(structured_feeds)

        # To get thumbnails from the ImageView elements, it seems the best way
        # for now is to crop screenshots

        # https://stackoverflow.com/questions/13832322/how-to-capture-the-screenshot-of-a-specific-element-rather-than-entire-page-usin
        # media_elements = driver.find_elements(By.XPATH, '//android.widget.ImageView')
        # for elem in media_elements:
        #     print(elem)

        