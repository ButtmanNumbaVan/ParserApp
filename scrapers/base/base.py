import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.requests.session import Session
from abc import ABC, abstractmethod
import time


class BaseScraper(ABC):
    current_page = ''
    start_page_url = ''
    page_pattern_url = ''
    start_page_index = 0
    number_of_pages = 0

    def __init__(self):
        self.session = Session()
        self.driver = webdriver.Firefox()
        self.current_page_url = self.start_page_url

    def get_page_source_driver(self, url):
        page_source = ''
        while page_source == '':
            try:
                self.driver.get(url)
                page_source = self.driver.page_source
                break

            except:
                print("Connection refused by the server..")
                time.sleep(5)
                continue

        return page_source

    def get_page_source_session(self, url):
        page_source = ''
        while page_source == '':
            try:
                page_source = self.session.get(url, headers=self.session.headers)
                break

            except:
                print("Connection refused by the server..")
                time.sleep(5)
                continue

        return page_source.text

    def get_page_soup(self, url):
        page_source = self.get_page_source_driver(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def get_brand_name_from_item_name(self, item_name):
        brands = ['jordan', 'nike', 'adidas', 'under armour', 'ua']

        item_name = item_name.lower()

        for brand in brands:
            if brand in item_name:
                return brand

        return 'Unknown'

    @abstractmethod
    def get_pages_urls(self, *args):
        pages_number = self.get_number_of_pages()
        all_pages = []

        for pages_number in range(self.start_page_index, pages_number + 1):
            # for page_number in range(1, 1 + 1):
            url_to_scrap = self.page_pattern_url + str(page_number)
            # print(url_to_scrap)
            page_sneakers = self.parse_catalog_items(url_to_scrap)

        return all_pages

    @abstractmethod
    def get_number_of_pages(self):
        pass

    @abstractmethod
    def get_all_catalog_items(self, *args):
        pass

    @abstractmethod
    def get_sneaker_sizes(self, *args):
        pass

    @abstractmethod
    def get_article(self, *args):
        pass

    @abstractmethod
    def parse_catalog_items(self, *args):
        pass

    def scrap(self):
        pages_number = self.get_number_of_pages()
        all_sneakers = []

        for page_url in range(self.start_page_index, pages_number + 1):
            # for page_number in range(1, 1 + 1):
            url_to_scrap = self.page_pattern_url + str(page_number)
            # print(url_to_scrap)
            page_sneakers = self.parse_catalog_items(url_to_scrap)

            for sneaker in page_sneakers:
                all_sneakers.append(sneaker)

        return all_sneakers

