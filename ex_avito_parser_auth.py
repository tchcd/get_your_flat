# Аутентификация, кукисы

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pickle


def webdriver_cfg():
    options = webdriver.ChromeOptions()
    options.add_argument(
        f"user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--no-sandbox')
    options.headless = False
    driver = webdriver.Chrome(
        r"C:/Users/q/IdeaProjects/Python3/flatblet/chromedriver/chromedriver.exe",
        options=options,
    )

    return driver


def auth_avito(url="https://www.avito.ru"):

    driver.get(url)
    time.sleep(2)

    for cookie in pickle.load(
        open(r"C:\Users\q\IdeaProjects\Python3\flatblet\session", "rb")
    ):
        driver.add_cookie(cookie)
    time.sleep(2)
    driver.get(url)
    time.sleep(2)
