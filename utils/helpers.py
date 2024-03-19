from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from pydantic import ValidationError
from selenium import webdriver
from .const import *
import requests
import random
import time
import os


def configure_webdriver(open_browser=False, block_media=False, block_elements=['css', 'img', 'js']):
    options = webdriver.ChromeOptions()

    # Install the extension
    extension_path = 'utils/pia.crx'

    if not open_browser:
        options.add_argument("--headless=new")
    if block_media:
        hide_elements = {
            'plugins': 2, 'popups': 2, 'geolocation': 2, 'notifications': 2,
            'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2, 'mixed_script': 2,
            'media_stream': 2, 'media_stream_mic': 2, 'media_stream_camera': 2,
            'protocol_handlers': 2, 'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
            'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2,
            'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2
        }
        if 'cookies' in block_elements:
            hide_elements.update({'cookies': 2})
        if 'js' in block_elements:
            hide_elements.update({'javascript': 2})
        if 'img' in block_elements:
            hide_elements.update({'images': 2})
        prefs = {'profile.default_content_setting_values': hide_elements}
        options.add_argument('--disable-features=EnableNetworkService')
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_experimental_option('prefs', prefs)
    options.add_argument("window-size=1200,1100")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")

    options.add_extension(extension_path)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    if block_media:
        # Enable Chrome DevTools Protocol
        driver.execute_cdp_cmd("Page.enable", {})
        driver.execute_cdp_cmd("Network.enable", {})

        # Set blocked URL patterns to disable images and stylesheets
        blocked_patterns = []
        if 'img' in block_elements:
            blocked_patterns.extend(["*.jpg", "*.jpeg", "*.png", "*.gif", ])
        if 'css' in block_elements:
            blocked_patterns.extend(["*.css"])
        if 'js' in block_elements:
            blocked_patterns.extend(["*.js"])
        driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": blocked_patterns})
    return driver

def make_plural(word: str = '', num: int = 1) -> str:
    return word + 's' if word and word.strip() and (num > 1 or num == 0) else word


def validation_err_msg(Error: ValidationError) -> str:
    msg = ''
    if Error:
        for error in Error.errors():
            msg += error['msg'] + '\n'
    return msg


def upload_jobs_to_octagon(payload) -> bool:
    try:
        base_url = os.getenv("OCTAGON_API_URL")
        url = f"{base_url}/flask/post-jobs/"
        headers = {
            "content-type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        return response.status_code == 200

    except Exception as e:
        print(str(e))
        return False

def set_job_type(job_type, sub_type="remote"):
    if 'full time' in job_type.lower() and sub_type == 'remote':
        return JOB_TYPE[0]
    elif 'full time' in job_type.lower() and sub_type == 'onsite':
        return JOB_TYPE[1]
    elif 'full time' in job_type.lower() and sub_type == 'hybrid':
        return JOB_TYPE[2]
    elif 'contract' in job_type.lower() and sub_type == 'remote':
        return JOB_TYPE[5]
    elif 'contract' in job_type.lower() and sub_type == 'onsite':
        return JOB_TYPE[4]
    elif 'contract' in job_type.lower() and sub_type == 'hybrid':
        return JOB_TYPE[3]
    else:
      return job_type.capitalize()
    
def k_conversion(text):
    return text.replace("k", ",000").replace( "K", ",000")

def change_pia_location(driver, location=None, extension_opened=False, undetected=False) -> bool:
    error_status = False
    try:
        if not extension_opened:
            driver.get(get_pia_web_url(undetected))
        driver.find_element(By.CLASS_NAME, 'region-content').click()
        # if no location found then select US Miami
        if location:
            driver.find_element(By.CLASS_NAME, 'region-search-input').send_keys(location)
            driver.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "ul").click()
        else:
            driver.find_element(By.CLASS_NAME, 'region-search-input').send_keys("US ")
            us_locations = [location_btn for location_btn in driver.find_elements(By.CLASS_NAME, "region-list-item")[1:]]
            if us_locations:
                random_location = random.randrange(len(us_locations))
                us_locations[random_location].click()
            else:
                driver.find_element(By.CLASS_NAME, 'region-search-input').send_keys("US Miami")
                driver.find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "ul").click()
        time.sleep(5)
    except Exception as e:
        error_status = True
        print(str(e))
    return error_status

def get_pia_web_url(undetected=False):
    pia_extension_id = PIA_UNPACKED_EXTENSION_ID if undetected else PIA_CRX_EXTENSION_ID
    pia_web_url = f"chrome-extension://{pia_extension_id}/html/foreground.html"
    return pia_web_url


# pia extension ids
PIA_CRX_EXTENSION_ID = 'jplnlifepflhkbkgonidnobkakhmpnmh'
PIA_UNPACKED_EXTENSION_ID = 'olfblhmobjbfckldmpdgehfecmjapkob'
def determine_job_sub_type(type):
        sub_type = "remote"
        if "onsite" in type.strip().lower() or "on site" in type.strip().lower():
            sub_type = "onsite"
        if "hybrid" in type.strip().lower():
            sub_type = "hybrid"
        return sub_type

def k_conversion(text):
    return text.replace("k", ",000").replace( "K", ",000")

def determine_job_sub_type(type):
        sub_type = "remote"
        if "onsite" in type.strip().lower() or "on site" in type.strip().lower():
            sub_type = "onsite"
        if "hybrid" in type.strip().lower():
            sub_type = "hybrid"
        return sub_type

def k_conversion(text):
    return text.replace("k", ",000").replace( "K", ",000")