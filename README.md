# themistalkles
Scrape user public data to gain insights and produce a profile

### Setup

* [appium setup](https://github.com/appium/appium/blob/master/docs/en/about-appium/getting-started.md)
* Android Studio, virtual device Nexus 5X API 28 x86
* Apk binary mirror: [instagram](https://www.apkmirror.com/apk/instagram/instagram-instagram/instagram-instagram-70-0-0-22-98-130580-release/instagram-70-0-0-22-98-4-android-apk-download/)
* pytest

### What to expect

##### Instagram automation

* given `credentials/insta.json` containing
```
{
    "username": "xxx",
    "password": "yyy"
}
```
* run `cd src; ./insta.py` and the automated test will log in, go to 'activity' -> 'following', and collect the text feeds since 1 day ago, and store them in `./src/feeds/`, in [a structured format](src/parse.t.py#L40).

### Troubleshooting

* appium takes a long time to connect inspector / run app: check environment variable proxy setting
* [activity startup](https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/android/activity-startup.md#how-to-troubleshoot-activities-startup): to figure out `appWaitActivity` and `appWaitPackage`, run this the window is active:
```
adb shell dumpsys window windows | grep -i activity
```
* Appium device inspector: use [capabilities json](instagram_session.json) to inspect instagram
* apk abi mismatch: emulator abi (x86, arm, etc) needs to match apk abi
```
INSTALL_FAILED_NO_MATCHING_ABIS: Failed to extract native libraries, res=-113
```