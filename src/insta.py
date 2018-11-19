#!/usr/bin/env pytest

import pytest
import os
import textwrap
import json
from datetime import datetime
import logging

from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from helpers import take_screenhot_and_logcat, EXECUTOR, get_structured_feeds, json_serial

class TestAndroidBasicInteractions():
    PACKAGE = 'com.instagram.android'
    MAIN_ACTIVITY = '.activity.MainTabActivity'
    WAIT_ACTIVITY = 'com.instagram.nux.activity.SignedOutFragmentActivity'

    # XPATH leads to fragile tests, unideal but no immediate workaround
    HEART_XPATH = '//android.widget.FrameLayout[@content-desc="Activity"]'
    FOLLOWING_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[1]'
    YOU_XPATH = '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.TextView[2]'

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

        curr_wait = wait.until(EC.element_to_be_clickable((By.XPATH, self.YOU_XPATH)))
        # following_button = driver.find_element(By.XPATH, self.FOLLOWING_XPATH)
        # following_button.click()
        # due to lack of element to decide whether we are ready to click 'following',
        # we use a swipe right once on 'activity' page
        driver.swipe(230, 850, 750, 850, 330)

        # record feeds in 'following'
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

        scroll_further = True
        while scroll_further:
            driver.swipe(470, 1400, 470, 950, 330)
            scroll_further = record_feeds(driver, text_feeds)

        # done with feeds, log raw and structured to files
        text_feeds_file = 'feeds/text_feeds_' + str(datetime.now()) + '.log'
        with open(text_feeds_file, 'w') as writefile:
            writefile.write(str(text_feeds))

        # process structured feeds
        structured_feeds = get_structured_feeds(text_feeds)
        structured_feeds_file = 'feeds/structured_feeds_' + str(datetime.now()) + '.log'
        with open(structured_feeds_file, 'w') as writefile:
            writefile.write(json.dumps(structured_feeds, default = json_serial))

        # To get thumbnails from the ImageView elements, it seems the best way
        # for now is to crop screenshots

        # https://stackoverflow.com/questions/13832322/how-to-capture-the-screenshot-of-a-specific-element-rather-than-entire-page-usin
        # media_elements = driver.find_elements(By.XPATH, '//android.widget.ImageView')
        # for elem in media_elements:
        #     print(elem)

        