import time
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC


def scroll_by(driver, delta):
    webdriver.ActionChains(driver).scroll_by_amount(0, delta).perform()


def scroll_to_ad(driver, ad, delta):
    webdriver.ActionChains(driver).scroll_to_element(ad).perform()
    scroll_by(driver, delta)


def sponsoring_available(driver, target):
    # if available make object
    try:
        return driver.find_element(By.XPATH, target)
    except Exception as e:
        print(f"No such object: {target}. Error code: {e}")
        return ""


def sponsoring_unroll(driver, ad, screenshot_dir, site_name, name, sequence, collapse):
    # open-screenshot-close
    try:
        ad.click()
        time.sleep(3)
        take_screenshot(screenshot_dir, site_name, sequence, name)
        driver.find_element(By.XPATH, collapse).click()
        time.sleep(2)
    except Exception as e:
        print(f"No expand/collapse element available: {name} at page {site_name}.")
        print(f"Error code: {e}")
        pass


def make_target_ads(driver, name, target, branding_ads):
    # creates object targeted by xpath
    if name in branding_ads:
        return sponsoring_available(driver, target)
    else:
        try:
            return driver.find_element(By.XPATH, target)
        except Exception as e:
            print(f"No such object: {target}. Error code: {e}")
            pass


def take_screenshot(path, portal, sequence, name):
    screenshot = pyautogui.screenshot()
    screenshot.save(f'{path}\\{portal}-{name}-{sequence + 1}.png')
    time.sleep(1)


def core_loop_fun(portal_name, sponsors_tup, targets_dict, scrolls_dict, branding_ads):
    for sequence in range(8):
        ads_sg = {}
        for name, target in targets_dict.items():
            destination = make_target_ads(driver, name, target, branding_ads)
            ads_sg[name] = destination
        for name, ad in ads_sg.items():
            delta = scrolls_dict.get(name)
            if name == list(scrolls_dict.keys())[0]:
                sponsoring_unroll(
                    driver, ad, screenshot_path, portal_name, name, sequence, sponsors_tup[1])
                continue
            try:
                scroll_to_ad(driver, ad, delta)
            except Exception as e:
                print(f'Error at site: {site}, at ad: {ad} \
                with movement of {delta} pixels. Error message: {e}')
            time.sleep(2)
            take_screenshot(screenshot_path, portal_name, sequence, name)
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(4)
        driver.refresh()
        ads_sg.clear()
        time.sleep(1)


brandings = ("sponsor_d", "ppremium_d", "branding_d", "premiumboard_d", "topboard_d")

try:
    os.mkdir(".\\screenshots")
except FileExistsError as e:
    print(e)

screenshot_path = f"{os.getcwd()}\\screenshots"

mobile_emulation = {"deviceName": "iPhone 12 Pro"}

# Setup driver
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument('--start-maximized')
options.add_argument("--force-device-scale-factor=1")
options.add_experimental_option("mobileEmulation", mobile_emulation)
# options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) \
#                      AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 \
#                      Safari/604.1')
# use the line below if cookies are needed
# options.add_argument(f"--user-data-dir={os.getcwd()}\\cookies_scr_taker")


# driver = webdriver.Chrome(options=options, service=Service(
#     ChromeDriverManager().install()))


# use if webdriver_manager fails
# give path to webdriver on your hard drive
driver_path = "C:\\WebDriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, service=Service(driver_path))

driver.get("https://www.filmweb.pl/")
driver.implicitly_wait(5)

# %% FILMWEB SG
# accept cookies
try:
    cookie = driver.find_element(By.XPATH, "//button[@id='didomi-notice-agree-button']")
    cookie.click()
    time.sleep(1.25)
except Exception:
    print("No cookies to accept")

# time.sleep(5)

site = "filmweb"

# when sponsor available locate expand collapse buttons

# expand, collapse pairs in tuples
sponsors = ("//div[@class='faSponsoring__btn']", "//div[@class='faSponsoring__btn']")  # ok

targets = {
    "sponsoring_d": "//div[@class='faSponsoring__btn']",  # ok
    "screening": "//div[@style='position: relative;']//div[contains(@class, 'fa__slot fa__slot')]",
    }


scrolls = {
    "sponsoring": 0,
    "screening": 0,
    }


# filmweb sg traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)







