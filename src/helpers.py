import os
import re
from datetime import datetime, timedelta

from selenium.common.exceptions import InvalidSessionIdException

ANDROID_APP_PATH = 'http://appium.github.io/appium/assets/ApiDemos-debug.apk' if os.getenv(
    'SAUCE_LABS') else os.path.abspath('../bin/instagram-70-0-0-22-98.apk')

IOS_APP_PATH = 'http://appium.github.io/appium/assets/TestApp7.1.app.zip' if os.getenv(
    'SAUCE_LABS') else os.path.abspath('../apps/TestApp.app.zip')

if os.getenv('SAUCE_USERNAME') and os.getenv('SAUCE_ACCESS_KEY'):
    EXECUTOR = 'http://{}:{}@ondemand.saucelabs.com:80/wd/hub'.format(
        os.getenv('SAUCE_USERNAME'), os.getenv('SAUCE_ACCESS_KEY'))
else:
    EXECUTOR = 'http://127.0.0.1:4723/wd/hub'


def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def take_screenhot_and_logcat(driver, device_logger, calling_request):
    __save_log_type(driver, device_logger, calling_request, 'logcat')


def take_screenhot_and_syslog(driver, device_logger, calling_request):
    __save_log_type(driver, device_logger, calling_request, 'syslog')


def __save_log_type(driver, device_logger, calling_request, type):
    logcat_dir = device_logger.logcat_dir
    screenshot_dir = device_logger.screenshot_dir

    try:
        driver.save_screenshot(os.path.join(screenshot_dir, calling_request + '.png'))
        logcat_data = driver.get_log(type)
    except InvalidSessionIdException:
        logcat_data = ''

    with open(os.path.join(logcat_dir, '{}_{}.log'.format(calling_request, type)), 'wb') as logcat_file:
        for data in logcat_data:
            data_string = '{}:  {}'.format(data['timestamp'], data['message'])
            logcat_file.write((data_string + '\n').encode('UTF-8'))

def get_structured_feeds(text_feeds, offset_time = datetime.now()):
    structured_feeds = []
    CONJUNCTION = 'and'

    for feed in text_feeds:
        parts = feed.split()

        time = parts[-1].strip()
        
        subject = [parts[0].strip()]
        rest_idx = 1

        # a and b liked c's post. 2h
        # TODO: this does not account for 'a, b, and 3 others liked c's post
        if len(parts) > 1 and parts[1] == CONJUNCTION:
            rest_idx = 3
            subject.append(parts[2])

        text = ' '.join(parts[rest_idx:-1])
        text.strip()

        post_time = offset_time
        if time.endswith('d'):
            post_time = offset_time - timedelta(days = int(time[:-1]))
        elif time.endswith('h'):
            post_time = offset_time - timedelta(hours = int(time[:-1]))
        elif time.endswith('m'):
            post_time = offset_time - timedelta(minutes = int(time[:-1]))
        elif time.endswith('s'):
            post_time = offset_time - timedelta(seconds = int(time[:-1]))
        else:
            print('unrecognized time format: ' + time)

        actions = ['liked', 'started following', 'shared']

        def parse_following(text):
            targets = text.split(',')
            and_targets = targets[-1].split()
            res = [target.strip() for target in targets[:-1]]
            if len(and_targets) >= 3 and and_targets[1].strip() == CONJUNCTION:
                res.append(and_targets[0])
                
                if len(and_targets) > 3:
                    count = int(and_targets[2])
                    res += ['unknown' for i in range(count)]
                else:
                    res.append(and_targets[2].rstrip('.'))
            return res

        patterns = [{
                # liked c's post.
                'string': actions[0] + " ([^' ]*?)'s posts?.",
                'action': lambda x : {
                    'action': actions[0].replace(' ', '_'),
                    'target': [x.group(1)]
                }
            }, {
                # liked x posts.
                'string': actions[0] + ' ([0-9]+) posts?.',
                'action': lambda x : {
                    'action': actions[0].replace(' ', '_'),
                    'count': int(x.group(1))
                }
            }, {
                # started following a, b, c.
                # started following a, b, and x others.
                'string': actions[1] + ' (.*)',
                'action': lambda x : {
                    'action': actions[1].replace(' ', '_'),
                    'target': parse_following(x.group(1))
                }
            }, {
                # shared x posts at l.
                'string': actions[2] + ' ([0-9]+) posts at ([^ ]*?)',
                'action': lambda x : {
                    'action': actions[2].replace(' ', '_'),
                    'count': int(x.group(1)),
                    'target': [x.group(2)]
                }
            }]
        
        match_found = False
        structured_feed = {}

        for pattern in patterns:
            res = re.match(pattern['string'], text)
            if res:
                match_found = True
                structured_feed = pattern['action'](res)
                break

        if not match_found:
            print('failed to match: ' + text)
        structured_feed['time'] = post_time
        structured_feed['subject'] = subject

        structured_feeds.append(structured_feed)

    return structured_feeds
