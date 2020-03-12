import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
import time


class SklepKoszykarza:
    def __init__(self):
       # self.session = Session()
        self.start_page_url = 'https://sklepkoszykarza.pl/products/obuwie/category,2/item,72/page,1'
        self.page_pattern_url = 'https://sklepkoszykarza.pl/products/obuwie/category,2/item,72/page,'
        self.start_page_index = 1
        self.current_page_url = self.start_page_url
        self.driver = webdriver.Firefox()
        #self.all_sneakers = []

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
                print('Sklep')
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

        number_of_pages = int(soup.find(class_='pagination__input').find('span').text[-1])
        print(number_of_pages)

        return number_of_pages

    def get_all_catalog_items(self, url):
        soup = self.get_page_soup(url)
        #print(soup)
        catalog_items = soup.find(id='filter__products').find_all(class_='col-sm-6 col-md-4 col-xs-12 product')
       # print(len(catalog_items))
        return catalog_items

    def get_sneaker_sizes(self, item):
        sizes = []
        sizes_from_container = item.find(class_='sizes').find_all('li')
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
        sneakers = []

        for item in catalog_items:
            sneaker = []
            sneaker_name = item.find(class_='n').text.replace('\n', "")
            sneaker_price = float(re.findall(r'\d+[,.]\d+', item.find(class_='ps pricebox').text.replace(',', '.'))[0])
            sneaker_article = item.find(class_='s').find('span').text.lower()
            sneaker_sizes = self.get_sneaker_sizes(item)
            sneaker_url = item.find('a')['href']

            sneaker_brand = self.get_brand_name_from_item_name(sneaker_name)

            try:
                sneaker_image_url = item.find('img')['data-echo']
            except:
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

        for i in range(1, pages_number+1):
        #for i in range(1, 1 + 1):
            url_to_scrap = self.page_pattern_url + str(i)
            page_sneakers = self.parse_catalog_items(url_to_scrap)

            for sneaker in page_sneakers:
                all_sneakers.append(sneaker)

       # print(len(all_sneakers))
        return all_sneakers