from selenium import webdriver
from bs4 import BeautifulSoup
from utils.requests.session import Session
import time
import re
import pickle
import requests


class Ataf:
    def __init__(self):
        self.session = Session()
        self.start_page_url = 'https://www.ataf.pl/854-buty-do-koszykowki?&page=1'
        self.page_pattern_url = 'https://www.ataf.pl/854-buty-do-koszykowki?&page='
        self.start_page_index = 1
        self.current_page_url = self.start_page_url
        self.driver = webdriver.Firefox()

    def get_page_source(self, url):
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

    def get_page_source_fast(self, url):
        page_source = ''
        while page_source == '':
            try:
                page_source = self.session.get(url, headers = self.session.headers)
                break

            except:
                print("Connection refused by the server..")
                time.sleep(5)
                continue

        return page_source.text

    def get_page_soup(self, url):
        page_source = self.get_page_source(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def get_number_of_pages(self):
       #  soup = self.get_page_soup(self.start_page_url)
       #
       #  number_of_pages = int(soup.find(class_='pagination__input').find('span').text[-1])
       # # print(number_of_pages)

        return 5

    def get_all_catalog_items(self, url):
        soup = self.get_page_soup(url)
        catalog_items = soup.find(class_='pcajax row').find_all(class_='col-md-6 col-lg-4 no-pad')

        return catalog_items

    def get_sneaker_sizes(self, item):
        sizes = []
        sizes_from_container = item.find_all('span')

        for size in sizes_from_container:
            sizes.append(size.text[3:])

        return sizes

    def get_article(self, item_url):
        soup = BeautifulSoup(self.get_page_source_fast(item_url), 'html.parser')
        article = soup.find(string="Kod produktu:").find_next('td').contents[0]

        return article

    def get_brand_name_from_item_name(self, item_name):
        brands = ['jordan', 'nike', 'adidas', 'under armour', 'ua']

        item_name = item_name.lower()

        for brand in brands:
            if brand in item_name:
                return brand

        return 'Unknown'

    def parse_catalog_items(self, url):
        catalog_items = self.get_all_catalog_items(url)
        sneakers = []

        for item in catalog_items:
            sneaker = []

            sneaker_name = item.find(class_='slider-product').text
            sneaker_price = float(re.findall(r'\d+[,.]\d+', item.find(class_='slider-price').text.replace(',', '.'))[0])
            sneaker_url = item.find('a')['href']
            sneaker_article = self.get_article(sneaker_url).lower()
            sneaker_sizes = self.get_sneaker_sizes(item)

            sneaker_brand = self.get_brand_name_from_item_name(sneaker_name)

            try:
                sneaker_image_url = item.find('img')['src']
            except:
                sneaker_image_url = 'No image'

            print(sneaker_name)
            print(sneaker_price)
            print(sneaker_brand)
            print(sneaker_image_url)

            sneaker.append(sneaker_name)
            sneaker.append(sneaker_price)
            sneaker.append(sneaker_article)
            sneaker.append(sneaker_url)
            sneaker.append(sneaker_brand)
            sneaker.append(sneaker_image_url)
            sneaker.append(sneaker_sizes)

            sneakers.append(sneaker)

        return sneakers

    def scrap(self):
        pages_number = self.get_number_of_pages()
        all_sneakers = []

        for page_number in range(1, pages_number+1):
        #for page_number in range(1, 1 + 1):
            url_to_scrap = self.page_pattern_url + str(page_number)
            #print(url_to_scrap)
            page_sneakers = self.parse_catalog_items(url_to_scrap)

            for sneaker in page_sneakers:
                all_sneakers.append(sneaker)

        return all_sneakers