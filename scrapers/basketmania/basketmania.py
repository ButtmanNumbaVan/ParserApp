from selenium import webdriver
from bs4 import BeautifulSoup
from utils.requests.session import Session
#from utils.spreadsheets.googlespreadsheet import SpreadSheet
#from parsers.sklepkoszykarza.sneakersgetter import SklepKoszykarza
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from scrapers.base.base import BaseScraper
from utils.decorators import error_catcher
import re


class BasketManiaScraper(BaseScraper):
    item_pattern_url = 'https://basketmania.pl'

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)

    def get_number_of_pages(self):
        super().get_number_of_pages()

    def get_page_soup(self, url):
        page_source = self.driver.get_page_source_scroll_mania(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def get_all_page_item_containers(self, url):
        soup = self.get_page_soup(url)
        catalog_items = soup.find(class_='main_hotspot').find_all(class_=re.compile("^product_wrapper"))

        return catalog_items

    @error_catcher
    def get_sneaker_sizes(self, container):
        #url = self.get_sneaker_url(container)
        soup = BeautifulSoup(self.driver.firefox.page_source, 'html.parser')

        sizes = []
        sizes_from_container = soup.find(class_='fsp_eur').find_all(class_=re.compile("^fsp_element"))
        # print(sizes_from_container)

        for size in sizes_from_container:
            # print(size['class'])
            if 'disabled' not in size['class']:
                sizes.append(size.text)

        return sizes

    @error_catcher
    def get_sneaker_article(self, container):
        url = self.get_sneaker_url(container)
        soup = BeautifulSoup(self.driver.get_page_source_driver(url), 'html.parser')

        article = soup.find(string="Kod produktu: ").find_next('strong').contents[0]

        return article

    @error_catcher
    def get_sneaker_name(self, container):
        return container.find(class_='product-name').text

    @error_catcher
    def get_sneaker_price(self, container):
        return float(re.findall(r'\d+[,.]\d+', container.find(class_='price').text.replace(',', '.'))[0])

    @error_catcher
    def get_sneaker_url(self, container):
        return self.item_pattern_url + container.find('a')['href']

    @error_catcher
    def get_sneaker_image_url(self, container):
        return self.item_pattern_url + container.find('img')['data-src']

    def get_all_urls(self):
        return ['https://basketmania.pl/pol_m_Buty-149.html']

    @error_catcher
    def get_brand_name_from_item_name(self, container):
        return container.find(class_='firm-name').find('a').text


# mania = BasketMania()
# mania.scrap()