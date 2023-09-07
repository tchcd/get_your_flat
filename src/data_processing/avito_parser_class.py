from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from src.logcfg import logger_cfg
import logging
from src import exceptions as exc
import pickle
import random
import time
import re
import cfg


logging.config.dictConfig(logger_cfg)
logger = logging.getLogger('logger')

RAND_TIME = random.uniform(1, 2.5)


class AvitoParser:
    def __init__(self, headless: bool):
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
        self.driver = webdriver.Remote(command_executor="http://selenium-hub:4444/wd/hub",
                                       options=self.options)
        #self.driver = webdriver.Chrome(r"C:\Users\q\IdeaProjects\Python3\flatblet\chromedriver\chromedriver.exe", options=self.options)
        self.driver.implicitly_wait(5)
        self.rand_time = RAND_TIME
        self.storage = []

    def _auth(self):
        """Avito user authentication"""
        self.driver.get(self.url)
        for cookie in pickle.load(open(cfg.SESSION, "rb")):
            self.driver.add_cookie(cookie)
        self.driver.get(self.url)
        return self

    def _handle_properties(self):
        """Collect flat listing properties"""
        try:
            time.sleep(RAND_TIME)
            properties_list = {}

            # Get subway
            properties_list["subway"] = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#app > div > div.index-root-nb9Lx.index-responsive-yh9uW.index-page_default-RyjXj > div > div.style-item-view-PCYlM.react-exp > div.style-item-view-content-SDgKX > div.style-item-view-content-left-bb5Ih > div.style-item-view-main-tKI1S.js-item-view-main.style-item-min-height-TJwyJ > div.style-item-view-block-SEFaY.style-item-view-map-rppAn.style-opened-bPigk.style-new-style-iX7zV > div > div.style-item-map-location-wbfMT > div.style-item-address-KooqC > div > div > span > span:nth-child(1) > span:nth-child(2)"
            )[0].text

            # Get distance_to_subway_km
            distance_to_subway_km = self.driver.find_elements(
                By.CSS_SELECTOR,
                "#app > div > div.index-root-nb9Lx.index-responsive-yh9uW.index-page_default-RyjXj > div > div.style-item-view-PCYlM.react-exp > div.style-item-view-content-SDgKX > div.style-item-view-content-left-bb5Ih > div.style-item-view-main-tKI1S.js-item-view-main.style-item-min-height-TJwyJ > div.style-item-view-block-SEFaY.style-item-view-map-rppAn.style-opened-bPigk.style-new-style-iX7zV > div > div.style-item-map-location-wbfMT > div.style-item-address-KooqC > div > div > span > span:nth-child(1) > span.style-item-address-georeferences-item-interval-ujKs2")
            properties_list["minutes_to_subway"] = int(re.findall("(\d+)", distance_to_subway_km[0].text)[-1])

            # Get price
            properties_list["price"] = int(self.driver.find_elements(
                By.CLASS_NAME, "style-item-price-text-_w822")[0].text.replace(" ",""))

            # Get address
            address = self.driver.find_element(
                By.CLASS_NAME, "style-item-address__string-wt61A"
            ).text
            properties_list["address"] = address

            # Get time
            properties_list["time"] = self.driver.find_element(
                By.CLASS_NAME, "style-item-footer-Ufxh_"
            ).text

            # Get properties about house
            house = self.driver.find_elements(
                By.CLASS_NAME, "style-item-params-list-vb1_H"
            )
            for items in house:
                house_properties_list = items.text.split("\n")
                for obj in house_properties_list:
                    column, value = obj.split(":")[0], obj.split(":")[1]
                    properties_list[column] = value.strip()

            # Get properties about flat
            flat = self.driver.find_elements(By.CLASS_NAME, "params-paramsList-zLpAu")
            for items in flat:
                flat_properties_list = items.text.split("\n")
                for obj in flat_properties_list:
                    column, value = obj.split(":")[0], obj.split(":")[1]
                    properties_list[column] = value.strip()

            # Get link
            properties_list["link"] = f"{self.driver.current_url}"
        except:
            logger.info("EXCEPT HANDLING PROPERTIES")
            return None
        else:
            return properties_list

    def _set_filters(self):
        """Add filters for search on avito homepage"""
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

    def _get_pages(self, count_url):
        """ Generation correct link-path for parser"""
        page_range = [i for i in range(1, count_url+1)]
        cur_page = self.driver.current_url
        pages = []
        for num in page_range:
            pages.append(f"{cur_page[:-6]}&p={num}&s=104")
        logger.info(f'ALL READY PAGES - {pages}')
        return pages

    def _parse_objects(self, pages: list) -> None:
        """Start parsing from first page to given "MAX_URL_LINKS" page"""
        for page_url in pages:
            logger.info(f"CURRENT PAGE: {page_url}")
            self.driver.get(page_url)

            # Get links on objects from page
            links = self.driver.find_elements(By.CLASS_NAME, "iva-item-root-_lk9K")

            for obj in range(len(links)):
                logger.info(F"COLLECTING {obj} LINK")
                try:
                    links[obj].click()
                    time.sleep(RAND_TIME)
                    self.driver.switch_to.window(self.driver.window_handles[1])
                    data = self._handle_properties() # Start collection data from object
                    if data is not None:
                        self.storage.append(data)
                        logger.info(f"{obj} LINK HAS BEEN COLLECTED")
                    time.sleep(RAND_TIME)
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                except:
                    logger.info(f"{obj} LINK WAS NOT COLLECTED {links[obj]}")

    def start_parser(self, count_url: cfg.PAGES_TO_PARSE_NUM) -> list:
        """
        Run the parser

        :param count_url: number of generated pages for the parser
        :return: list of dictionaries with listing objects
        """
        try:
            self._auth()
            self._set_filters()
            pages_to_parse = self._get_pages(count_url=count_url)
            self._parse_objects(pages_to_parse)
        except Exception as err:
            raise exc.ParsingNotComplete from err
        else:
            return self.storage




