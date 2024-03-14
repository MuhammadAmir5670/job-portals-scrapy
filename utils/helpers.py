from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from pydantic import ValidationError
import requests
import os


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
        url = f"{base_url}/flask/flask-response/"
        headers = {
            "content-type": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
        return response.status_code == 200

    except Exception as e:
        print(str(e))
        return False
