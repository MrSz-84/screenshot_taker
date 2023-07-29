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


brandings = ("sponsor_d", "ppremium_d", "branding_d", "premiumboard_d", "topboard_d",
             "sponsoring_d")

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
# use the line below if cookies are needed
# options.add_argument(f"--user-data-dir={os.getcwd()}\\cookies_scr_taker")


# driver = webdriver.Chrome(options=options, service=Service(
#     ChromeDriverManager().install()))


# use if webdriver_manager fails
# give path to webdriver on your hard drive
driver_path = "C:\\WebDriver\\chromedriver.exe"
driver = webdriver.Chrome(options=options, service=Service(driver_path))


# %% ONET

# open site
driver.get("https://www.onet.pl/")
driver.implicitly_wait(5)

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

# open site
driver.get("https://www.wp.pl/")
driver.implicitly_wait(6)

# accept cookies
try:
    cookie = driver.find_element(By.XPATH, "//button[text()='AKCEPTUJĘ I PRZECHODZĘ DO SERWISU']")
    cookie.click()
    time.sleep(1.25)
except Exception:
    print("No cookies to accept")

try:
    cookie2 = driver.find_element(By.TAG_NAME, "svg")
    cookie2.click()
except Exception:
    print("No cookies to accept")

time.sleep(2)

site = "wp"

# expand, collapse pairs in tuples
sponsors = ("//div[@id='site-header']/div[1]/div[1]/img[contains(., scr)]",
            "//div[@id='site-header']/div[1]/div[1]/img[contains(., scr)]")

targets = {
    "ppremium_d": "//div[@id='site-header']/div[1]/div[1]/img[contains(., scr)]",  # ok
    "mdbb_d": "//div[contains(@class, 'sc-am7de8-1')]//a[contains(text(), 'TYM ŻYJE POLSKA')]",  # ok
    "hp_d": "//div[contains(@class, 'sc-b3pols-2')]",  # ok
    "baner_okazjonalny_d": "//aside[@class='sc-wc57lf-0 iTPMnl']//div[@data-st-area='Wiadomosci']/a",  # ok
    "midbox": "//div[@id='wp-weather-widget']//a[contains(text(), 'Prognoza')]",  # ok
    "hp_2_d": "//div[contains(@class, 'sc-oavu9q-0')]//div[contains(@class, 'sc-qhhnks-0')]/..",  # ok
    "content_box_sport_d": "//div[@data-section='sport']//div[contains(@class, 'sc-msqvd4-0')]/a[4]",  # ok
    "content_box_biz_d": "//div[@data-section='finances']//div[contains(@class, 'sc-1cnv2xe-3')]/div[1]",  # ok
    "content_box_gwiazdy_d": "//div[@data-section='celebrities']//div[contains(@class, 'sc-1cnv2xe-3')]/div[1]",  # ok
    "screening_moto_d": "//div[contains(@class, 'sc-11fiv62-0')]//a[contains(text(), 'Motoryzacja')]",  # ok
    }


scrolls = {
    "ppremium_d": 0,
    "mdbb_d": 0,
    "hp_d": 50,
    "baner_okazjonalny_d": 0,
    "midbox": 350,
    "hp_2_d": 0,
    "content_box_sport_d": 0,
    "content_box_biz_d": 100,
    "content_box_gwiazdy_d": 100,
    "screening_moto_d": 450,
    }

# wp traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)


# %% INTERIA

# open site
driver.get("https://www.interia.pl/")
driver.implicitly_wait(5)

# accept cookies
try:
    cookie = driver.find_element(By.XPATH, "//button[contains(text(), 'Przejdź do serwisu')]")
    cookie.click()
    time.sleep(1.25)
except Exception:
    print("No cookies to accept")

time.sleep(2)

site = "interia"

# expand, collapse pairs in tuples
sponsors = ("//span[@id='expandButtonCont']", "//span[@id='collapseButtonCont']")

targets = {
    "branding_d": "//span[@id='expandButtonCont']",
    "gorny_slot_d": "//div[@id='ad-gora_srodek']",
    "hp_dis_d": "//div[@id='ad-view-halfpage_wydarzenia']/../..",
    "hp_polecane_d": "//div[@id='ad-view-halfpage_wydarzenia_2']/../..",
    "baner_sport_d": "//a[contains(text(), 'Sport')]",
    "hp_sport_d": "//div[@id='ad-view-halfpage_sport']/../../..",
    "baner_biz_d": "//a[contains(text(), 'Biznes')]",
    "hp_biz_d": "//div[@id='ad-view-halfpage_biznes']/../../..",
    "baner_moto_d": "//a[contains(text(), 'Motoryzacja')]",
    }


scrolls = {
    "branding_d": 0,
    "gorny_slot_d": 0,
    "hp_dis_d": 0,
    "hp_polecane_d": 0,
    "baner_sport_d": 0,
    "hp_sport_d": 0,
    "baner_biz_d": 0,
    "hp_biz_d": 0,
    "baner_moto_d": 0,
    }

# interia traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)


# %% GAZETA

# open site
driver.get("https://www.gazeta.pl/0,0.html")
driver.implicitly_wait(5)

# accept cookies
try:
    cookie = driver.find_element(
        By.XPATH,
        "//button[@id='onetrust-accept-btn-handler']//span[contains(text(), 'AKCEPTUJĘ')]")
    cookie.click()
    time.sleep(1.25)
except Exception:
    print("No cookies to accept")

# time.sleep(5)

site = "gazeta"

# expand, collapse pairs in tuples
sponsors = ("//div[@id='openAds'][contains(., 'ROZWIŃ')]", "//div[@id='closeAds'][contains(., 'ZWIŃ')]")

targets = {
    "premiumboard_d": "//div[@id='openAds'][contains(., 'ROZWIŃ')]",
    "topboard_d": "//div[@class='timeline']//div[contains(text(), 'Najnowsze')]",
    "hp_d": "//div[@class='hotNews']",
    }


scrolls = {
    "premiumboard_d": 0,
    "topboard_d": 0,
    "hp_d": 75,
    }


# gazeta traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)


# %% SE

# open site
driver.get("https://www.se.pl/")
driver.implicitly_wait(5)

# accept cookies
try:
    cookie = driver.find_element(
        By.XPATH,
        "//button[contains(@class, 'shared-module_text-white')][text()[contains(., 'Akceptuję')]]")
    cookie.click()
    time.sleep(1.25)
except Exception:
    print("No cookies to accept")

# time.sleep(5)

site = "se"

# when sponsor available locate expand collapse buttons

# expand, collapse pairs in tuples
sponsors = ("", "")

targets = {
    "topboard_d": "",
    "mdbb_d": "//div[@id='hook_box_top1']",
    "hp_d": "//div[@class='gl_plugin listing']",
    }


scrolls = {
    "topboard_d": 0,
    "mdbb_d": 0,
    "hp_d": 0,
    }


# se traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)


# %% FILMWEB SG

# open site
driver.get("https://www.filmweb.pl/")
driver.implicitly_wait(5)

# accept cookies
try:
    cookie = driver.find_element(By.XPATH, "//button[@id='didomi-notice-agree-button']")
    cookie.click()
    time.sleep(1.55)
except Exception:
    print("No cookies to accept")


site = "filmweb"

# expand, collapse pairs in tuples
sponsors = ("//div[@class='faSponsoring__btn']", "//div[@class='faSponsoring__btn']")  # not ok

targets = {
    "sponsoring_d": "//div[@class='faSponsoring__btn']",  # not ok
    "screening": "//div[@style='position: relative;']//div[contains(@class, 'fa__slot fa__slot')]",
    }


scrolls = {
    "sponsoring": 0,
    "screening": 0,
    }


# filmweb traverse and screenshots
core_loop_fun(site, sponsors, targets, scrolls, brandings)
