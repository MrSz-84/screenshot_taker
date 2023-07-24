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


def core_loop_fun(portal_name, sponsors_tup, targets_dict, scrolls_dict, branding_ads, bottom_ads):
    for sequence in range(8):
        names_list = list(targets.keys())
        for name in names_list:
            target = targets_dict.get(name)
            destination = make_target_ads(driver, name, target, branding_ads)
            delta = scrolls_dict.get(name)
            if name in branding_ads:
                sponsoring_unroll(driver, destination, screenshot_path,
                                  portal_name, name, sequence, sponsors_tup[1])
                continue
            if name in bottom_ads:
                bottom_bars(driver, screenshot_path, portal_name, name, sequence, sponsors_tup[1])
                continue
            try:
                scroll_to_ad(driver, destination, delta)
            except Exception as e:
                print(f'Error at site: {site}, at ad: {destination} \
                with movement of {delta} pixels. Error message: {e}')
            time.sleep(3)
            take_screenshot(screenshot_path, portal_name, sequence, name)
            # dodać ruch ekranu w dół, aby ułatwić łapanie obiektu mobilnego
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(4)
        driver.refresh()
        time.sleep(1)


def bottom_bars(driver, screenshot_dir, site_name, name, sequence, collapse):
    try:
        take_screenshot(screenshot_dir, site_name, sequence, name)
        driver.find_element(By.XPATH, collapse).click()
        time.sleep(2)
    except Exception as e:
        print(f"No close element available: {name} at page {site_name}.")
        print(f"Error code: {e}")
        pass


brandings = ("sponsor_m", "ppremium_m", "branding_m", "premiumboard_m", "topboard_m")

bottoms = ("bottom_bar_m", )

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
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) \
                     AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 \
                     Safari/604.1')
# use the line below if cookies are needed
# options.add_argument(f"--user-data-dir={os.getcwd()}\\cookies_scr_taker")


# driver = webdriver.Chrome(options=options, service=Service(
#     ChromeDriverManager().install()))


# use if webdriver_manager fails
# give path to webdriver on your hard drive
driver_path = "C:\\WebDriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, service=Service(driver_path))

driver.get("https://www.interia.pl/")
driver.implicitly_wait(5)

# %% INTERIA
# accept cookies
try:
    cookie = driver.find_element(By.XPATH, "//button[contains(text(), 'Przejdź do serwisu')]")
    cookie.click()
    time.sleep(1.25)
except Exception:
    print("No cookies to accept")

site = "interia"

# expand, collapse pairs in tuples
sponsors = ("//span[@id='expandButtonCont']", "//span[@id='collapseButtonCont']")  # not ok

targets = {
    "branding_m": "//span[@id='expandButtonCont']",  # not ok
    "gorny_slot_m": "//a[contains(text(), 'Polecane')]",
    "hp_dis_m": "//div[@id='wydarzenia']//a[contains(text(), 'Wydarzenia')]",
    "baner_sport_m": "//a[contains(text(), 'Sport')]",
    "baner_biz_m": "//a[contains(text(), 'Biznes')]",
    "baner_moto_m": "//a[contains(text(), 'Motoryzacja')]",
    }


scrolls = {
    "branding_m": 0,
    "gorny_slot_m": 200,
    "hp_dis_m": 100,
    "baner_sport_m": 200,
    "baner_biz_m": 200,
    "baner_moto_m": 200,
    }


# interia traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings, bottoms)

