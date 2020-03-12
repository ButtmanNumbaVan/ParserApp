import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.requests.session import Session
import time


class Bakseto:
    def __init__(self):
       # self.session = Session()
        self.start_page_url = 'https://basketo.pl/pol_m_Obuwie_Buty-do-koszykowki-227.html#180'
        self.page_pattern_url = 'https://basketo.pl/pol_m_Obuwie_Buty-do-koszykowki-227.html#180'
        self.start_page_index = 1
        self.current_page_url = self.start_page_url
        self.driver = webdriver.Firefox()
        #self.all_sneakers = []

    def get_page_source(self, url, init=False):
        page_source = ''
        while page_source == '':
            try:
                print('here')
                if init:
                    self.driver.get('https://basketo.pl/settings.php?portions=180')
                self.driver.get(url)
                time.sleep(5)
                page_source = self.driver.page_source
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                print('Basketo')
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        self.current_page = url

        return page_source

    def get_page_soup(self, url):
        page_source = self.get_page_source(url, True)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def get_number_of_pages(self):
       #  soup = self.get_page_soup(self.start_page_url)
       #
       #  number_of_pages = int(soup.find(class_='pagination__input').find('span').text[-1])
       # # print(number_of_pages)

        return 1

    def get_all_catalog_items(self, url):
        soup = self.get_page_soup(url)
       # print(soup)
        catalog_items = soup.find_all(class_='product col-12 col-sm-4 col-md-3 pt-3 pb-md-3')
        #print(len(catalog_items))
        return catalog_items

    def get_sneaker_sizes(self, item):
        sizes = []
        sizes_from_container = item.find(class_='product__sizes mb-1').find_all('span')
        #print(sizes_from_container)

        for size in sizes_from_container:
            sizes.append(size.text)

        return sizes

    def get_brand_name_from_item_name(self, item_name):
        brands = ['jordan', 'nike', 'adidas', 'under armour', 'ua']

        item_name = item_name.lower()

        for brand in brands:
            if brand in item_name:
                return brand

        return 'Unknown'

    def parse_catalog_items(self, url):
        catalog_items = self.get_all_catalog_items(url)
        print(catalog_items)
        sneakers = []

        for item in catalog_items:
            sneaker = []
            sneaker_name = item.find(class_='product__name').text
            sneaker_price = float(re.findall(r'\d+[,.]\d+', item.find(class_='price').text.replace(',', '.'))[0])
            sneaker_article = sneaker_name.split(' ')[-1].lower()
            sneaker_url = 'https://basketo.pl' + item.find(class_='product__name')['href']
            sneaker_brand = self.get_brand_name_from_item_name(sneaker_name)

            try:
                sneaker_sizes = self.get_sneaker_sizes(item)
            except Exception as e:
                print('Size exception ', e)
                continue
            #more fields

            try:
                image = item.find('img')
                print(image.attrs.keys())
                if 'data-src' in image.attrs.keys():
                     sneaker_image_url = 'https://basketo.pl' + item.find('img')['data-src']
                elif 'src' in image.attrs.keys():
                     sneaker_image_url = 'https://basketo.pl' + item.find('img')['src']
                else:
                     sneaker_image_url = 'No image'
            except Exception as e:
                print(e)
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
       # pages_number = self.get_number_of_pages()
        all_sneakers = []


        url_to_scrap = self.page_pattern_url
        page_sneakers = self.parse_catalog_items(url_to_scrap)

        for sneaker in page_sneakers:
            all_sneakers.append(sneaker)

       # print(len(all_sneakers))
        return all_sneakers


# basketo = SklepKoszykarza()
# basketo.scrap()

# sklep = SklepKoszykarza()
# print(sklep.scrap())
# sklep.driver.close()
