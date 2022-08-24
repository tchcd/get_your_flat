from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from datetime import date, timedelta
from src.logcfg import logger_cfg
import logging
from src import exceptions
import pickle
import random
import time
import re


logging.config.dictConfig(logger_cfg)
log_error = logging.getLogger('log_error')
log_info = logging.getLogger('log_info')

RAND_TIME = random.uniform(1, 2.5)
MAX_URL_RANGE = 15  # How many urls page we take for parsing at all


class AvitoParser:
    def __init__(self, headless=False):
        """Create and launch selenium webdriver object"""
        self.url = "https://www.avito.ru/sankt-peterburg/kvartiry/prodam/vtorichka"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            f"user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0"
        )
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.headless = headless
        if self.headless:
            self.options.headless = True
            self.options.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(
            r"C:/Users/q/IdeaProjects/Python3/flatblet/chromedriver/chromedriver.exe",
            options=self.options,
        )
        self.rand_time = RAND_TIME
        self.storage = []

    def _auth_avito(self):
        """Avito user authentication"""
        self.driver.get(self.url)
        time.sleep(RAND_TIME)
        for cookie in pickle.load(open(r"C:\Users\q\IdeaProjects\Python3\flatblet\session", "rb")):
            self.driver.add_cookie(cookie)
        time.sleep(RAND_TIME)
        self.driver.get(self.url)
        return self

    def _handling_properties(self):
        """Collect flat listing properties"""
        properties_list = {}
        try:
            # Get subway
            properties_list["subway"] = self.driver.find_element(
                By.XPATH,
                """/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div[2]/div[2]/div/div[2]/div[1]
                /div/div/span/span[1]/span[2]""").text

            # Get distance
            distance = self.driver.find_elements(
                By.CLASS_NAME, "style-item-address-georeferences-item-18pFt"
            )
            properties_list["minutes_to_subway"] = int(
                re.findall(r"(\d+)", distance[0].text)[-1]
            )
            time.sleep(RAND_TIME)

            # Get price
            price = int(
                self.driver.find_elements(
                    By.CLASS_NAME, "style-price-value-main-1P7DJ"
                )[1]
                .find_element(By.CLASS_NAME, "js-item-price")
                .text.replace(" ", "")
            )
            properties_list["price"] = price if price else None
            time.sleep(RAND_TIME)

            # Get address
            address = self.driver.find_element(
                By.CLASS_NAME, "style-item-address__string-3Ct0s"
            ).text
            properties_list["address"] = address if address else None
            time.sleep(RAND_TIME)

            # Get time
            times = self.driver.find_elements(
                By.CLASS_NAME, "style-item-footer-3uXQz"
            ).text
            properties_list["time"] = times
            time.sleep(RAND_TIME)

            # Get properties about house
            house = self.driver.find_elements(
                By.CLASS_NAME, "style-item-params-list-3YJu7"
            )
            for items in house:
                house_properties_list = items.text.split("\n")
                for obj in house_properties_list:
                    column, value = obj.split(":")[0], obj.split(":")[1]
                    properties_list[column] = value.strip()

            # Get properties about flat
            flat = self.driver.find_elements(By.CLASS_NAME, "params-paramsList-2PiKQ")
            for items in flat:
                flat_properties_list = items.text.split("\n")
                for obj in flat_properties_list:
                    column, value = obj.split(":")[0], obj.split(":")[1]
                    properties_list[column] = value.strip()
            time.sleep(RAND_TIME)

            # Get link
            link = f"{self.driver.current_url}"
            properties_list["link"] = link if link else None
            time.sleep(RAND_TIME)
        except:                             # ошибка когда мы хотим обратится к объекту а его нет. Нужно ли ловить?
            log_info.info("EXCEPT HANDLING PROPERTIES")

        return properties_list

    def _get_filters(self):
        """Add filters for search on the avito homepage"""
        self.driver.find_elements(By.CLASS_NAME, "input-layout-stick-before-xYZY2")[0].send_keys("10000000" + Keys.ENTER)
        time.sleep(RAND_TIME)
        self.driver.find_elements(
            By.CLASS_NAME, "multi-select-checkbox-list-item-ub_Xu"
        )[2].click()
        time.sleep(RAND_TIME)
        self.driver.find_elements(
            By.CLASS_NAME, "multi-select-checkbox-list-item-ub_Xu"
        )[3].click()
        time.sleep(RAND_TIME)
        self.driver.find_element(By.CLASS_NAME, "styles-box-Up_E3").click()
        time.sleep(RAND_TIME)
        select = Select(
            self.driver.find_elements(By.CLASS_NAME, "select-select-IdfiC")[1]
        )
        select.select_by_index(3)
        return self

    def _pages_generation(self, count_url):
        """ Generation correct link-path for parser"""
        page_range = [i for i in range(1, count_url+1)]
        cur_page = self.driver.current_url
        pages = []
        for num in page_range:
            pages.append(f"{cur_page[:-6]}&p={num}&s=104")
        log_info.info(f'ALL READY PAGES - {pages}')
        return pages

    def _parse_objects(self, pages: list) -> None:
        """Start parsing from first page to given "MAX_URL_LINKS" page"""
        for page_url in pages:
            log_info.info(f"CURRENT PAGE: {page_url}")
            self.driver.get(page_url)
            time.sleep(RAND_TIME)

            # Get links on objects from page
            links = self.driver.find_elements(By.CLASS_NAME, "iva-item-root-_lk9K")
            time.sleep(RAND_TIME)

            for obj in range(len(links)):
                log_info.info(F"COLLECTING {obj} LINK")
                try:
                    links[obj].click()
                    time.sleep(RAND_TIME)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    data = (
                        self._handling_properties()
                    )  # Launch collection data from object
                    if data is not None:
                        self.storage.append(data)
                    time.sleep(RAND_TIME)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    log_info.info(f"{obj} LINK HAS BEEN COLLECTED")
                except:
                    log_info.info(f"{obj} LINK WAS NOT COLLECTED {links[obj]}")

    def start_parser(self, count_url: int = MAX_URL_RANGE) -> list:
        """
        Run the parser

        :param count_url: number of generated pages for the parser
        :return: list of dictionaries with listing objects
        """
        self._auth_avito()
        self._get_filters()
        pages_to_parse = self._pages_generation(count_url=count_url)
        self._parse_objects(pages_to_parse)

        return self.storage




