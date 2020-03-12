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


class BasketZone:
    def __init__(self):
        self.session = Session()
        self.start_page_url = 'https://basketzone.pl/index.php?action=przegladaj&kat=3&partia=0'
        self.page_pattern_url = 'https://basketzone.pl/index.php?action=przegladaj&kat=3&partia='
        self.start_page_index = 1
        self.current_page_url = self.start_page_url
        self.driver = webdriver.Firefox()
        #self.all_sneakers = []

    def get_page_source_fast(self, url):
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

    def get_page_source(self, url):
        page_source = ''
        while page_source == '':
            try:
                print('here')
                self.driver.get(url)
                page_source = self.driver.page_source
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                print('Zone')
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        self.current_page = url

        return page_source

    def get_page_soup(self, url):
        page_source = self.get_page_source(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def get_number_of_pages(self):
        soup = self.get_page_soup(self.start_page_url)

        number_of_pages = int(soup.find(class_='pages').find_all('span')[-1].find('a')['href'][-2:])
        print(number_of_pages)

        return number_of_pages

    def get_all_catalog_items(self, url):
        soup = self.get_page_soup(url)
        #print(soup)
        catalog_items = soup.find_all(class_='product size-on-product')
       # print(len(catalog_items))
        return catalog_items

    def get_sneaker_sizes(self, item):
        sizes = []
        sizes_from_container = item.find(class_='sizes-boxes').find_all('div')[-1].find_all('a')
        #print(sizes_from_container)

        for size in sizes_from_container:
            sizes.append(size.text)

        return sizes

    def get_article(self, item_url):
        soup = BeautifulSoup(self.get_page_source_fast(item_url), 'html.parser')
        article = soup.find(class_='product-page-indeks').text.replace(" ", "").replace("\n", "")

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
            sneaker_name = item.find(class_='name').text.replace("\n", "")
            sneaker_price = float(re.findall(r'\d+[,.]\d+', item.find(class_='prices clearfix').find_all('span')[-2].text.replace(',', '.'))[0])
            try:
                sneaker_sizes = self.get_sneaker_sizes(item)
            except:
                continue
            sneaker_url = item.find('a')['href']
            sneaker_article = self.get_article(sneaker_url).lower()
            sneaker_brand = self.get_brand_name_from_item_name(sneaker_name)

            try:
                sneaker_image_url = item.find('img')['src']
            except:
                sneaker_image_url = 'No image'

            #more fields
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

        for i in range(0, pages_number+1):
        #for i in range(0, 1):
            url_to_scrap = self.page_pattern_url + str(i)
            page_sneakers = self.parse_catalog_items(url_to_scrap)

            for sneaker in page_sneakers:
                all_sneakers.append(sneaker)

       # print(len(all_sneakers))
        return all_sneakers


# zone = BasketZone()
# zone.scrap()

# sklep = SklepKoszykarza()
# print(sklep.scrap())
# sklep.driver.close()
