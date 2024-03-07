import re
import time
import traceback
from datetime import datetime
from typing import List, Union
import pandas as pd
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, \
    ElementNotVisibleException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def configure_webdriver(open_browser=False):
    options = webdriver.ChromeOptions()
    if not open_browser:
        options.add_argument("--headless=new")
        options.add_argument("--disable-infobars")

    options.add_argument("window-size=1200,1100")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36")

    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=options)

    return driver


def make_plural(word: str = '', num: int = 1):
    return word + 's' if word and word.strip() and (num > 1 or num == 0) else word
