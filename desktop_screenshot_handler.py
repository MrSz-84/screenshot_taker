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
                with movmenet of {delta} pixels. Error message: {e}')
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

# Setup driver
options = Options()
options.add_experimental_option("detach", True)
options.add_argument("--disable-notifications")
options.add_argument('--start-maximized')
options.add_argument("--force-device-scale-factor=1")
# options.add_argument(f"--user-data-dir={os.getcwd()}\\cookies_scr_taker")

driver = webdriver.Chrome(options=options, service=Service(
    ChromeDriverManager().install()))

driver.get("https://www.onet.pl/")
driver.implicitly_wait(5)

# %% ONET
# accept cookies
try:
    cookie = driver.find_element(By.CSS_SELECTOR, "button[aria-label='accept and close']")
    cookie.click()
except Exception:
    print("No cookies to accept")

site = "onet"

# expand, collapse pairs in tuples
sponsors = ("//div[@class='btn expand']", "//div[@class='btn collapse']")

targets = {
    "sponsor_d": "//div[@class='btn expand']",
    "oim_d": "//div[@data-slotplhr='slot-top']",
    "tnim_d": "//h2[@title='Wiadomości']",
    "booster_d": "//div[@data-slotplhr='slot-right']",
    "odin1_d": "//div[@class='StandardRightFeed_othersWrap__aQxc2']//a[text()='Skarb Kibica']",
    "hp_2_d": "//div[@data-slotplhr='slot-right2']",
    "odin2_d": "//div[@class='StandardRightFeed_othersWrap__aQxc2']//a[text()='Kalkulator wynagrodzeń']",
    "hp_3_d": "//div[@data-slotplhr='slot-right2']//div[@id='right3stickydesktop']/../..",
    }

scrolls = {
    "sponsor_d": 0,
    "oim_d": 250,
    "tnim_d": 0,
    "booster_d": 0,
    "odin1_d": 0,
    "hp_2_d": 0,
    "odin2_d": 0,
    "hp_3_d": 0,
    }

# onet traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)


# %% WP


# sponsors = ("//*[@id='site-header']/div[1]/div[1]/div[3]", "//*[@id='site-header']/div[1]/div[1]/div[3]")
"""dodać slot midboxa!"""
# targets = {
#     "ppremium_d": "//*[@id='site-header']/div[1]/div[1]/div[3]",
#     "mdbb_d": "//*[@id='app-content']/div/div[2]/div",
#     "hp_d": "//*[@id='app-content']/div/div[3]/div[3]/div/div[2]/div",
#     "baner_okazjonalny_d": "//*[@id='app-content']/div/div[4]/div[1]/div/div/div[1]/div[1]",
#     "hp_2_d": "//*[@id='glonews']/div[4]/div[2]/aside/div[2]/div",
#     "content_box_sport_d": "//*[@id='app-content']/div/div[5]/div[2]",
#     "content_box_biz_d": "//*[@id='app-content']/div/div[7]/div[2]",
#     "content_box_gwiazdy_d": "//*[@id='app-content']/div/div[9]/div[2]",
#     "screening_moto_d": "//*[@id='app-content']/div/div[10]/div[3]/div[2]/div",
#     }


# driver.get("https://www.wp.pl/")
# driver.maximize_window()
# driver.implicitly_wait(5)
#
#
# # accept cookies
# cookie = driver.find_element(By.CSS_SELECTOR, "button[aria-label='accept and close']")
# cookie.click()


