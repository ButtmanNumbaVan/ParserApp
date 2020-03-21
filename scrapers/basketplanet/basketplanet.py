import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.requests.session import Session
from scrapers.base.base import BaseScraper
from utils.decorators import error_catcher
import time


#TODO:all scrapers should be abstarct based
class BasketPlanetScraper(BaseScraper):
    start_page_url = 'https://basketplanet.pl/pl/obuwie-meskie/'
    page_pattern_url = 'https://basketplanet.pl/pl/obuwie-meskie/?page='
    start_page_index = 1

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)

    def get_number_of_pages(self):
        soup = self.driver.get_page_soup(self.start_page_url)
        # print(soup)
        pages_number = int(soup.find(class_='page-list pagination justify-content-center justify-content-md-end'
                                            ' mt-3 mt-md-0').find_all('li')[-2].find('a').text)

        return pages_number

    def get_all_page_item_containers(self, url):
        soup = self.driver.get_page_soup(url)
        # print(soup)
        catalog_items = soup.find_all(class_='card card-product')
        # print(catalog_items)
        # print(len(catalog_items))
        # print('scrapping')
        return catalog_items

    @error_catcher
    def get_sneaker_article(self, container):
        article = container.find('img')['alt'].split(' ')[-1]
        print(article)
        return article

    @error_catcher
    def get_sneaker_sizes(self, container):
        sizes = []
        sizes_from_container = container.find(class_='sizeguide-avaiable-sizes').find_all('span')
        # print(sizes_from_container)

        for size in sizes_from_container:
            try:
                _ = size['class']
            except:
                sizes.append(size.text)

        print(sizes)

        return sizes

    @error_catcher
    def get_sneaker_name(self, container):
        return container.find(class_='h3 product-title').find('a').text

    @error_catcher
    def get_sneaker_price(self, container):
        #print(round(float(re.findall(r'\d+', container.find(itemprop='price').text)[0])/100))
        return round(float(re.findall(r'\d+', container.find(itemprop='price').text)[0])/100)

    @error_catcher
    def get_sneaker_url(self, container):
        return container.find('a')['href']

    @error_catcher
    def get_sneaker_image_url(self, container):
        return container.find('img')['src']


# class BasketPlanet:
#     def __init__(self):
#         self.session = Session()
#         self.start_page_url = 'https://basketplanet.pl/pl/3-obuwie-meskie#/page-1'
#         self.page_pattern_url = 'https://basketplanet.pl/pl/3-obuwie-meskie#/page-'
#         self.start_page_index = 1
#         self.current_page_url = self.start_page_url
#         self.driver = webdriver.Firefox()
#         #self.all_sneakers = []
#
#     def get_page_source_fast(self, url):
#         page_source = ''
#         while page_source == '':
#             try:
#                 page_source = self.session.get(url, headers=self.session.headers)
#                 break
#
#             except:
#                 print("Connection refused by the server..")
#                 time.sleep(5)
#                 continue
#
#         return page_source.text
#
#     def get_page_source(self, url):
#         page_source = ''
#         while page_source == '':
#             try:
#                 print('here')
#                 #self.driver.get('http://basketplanet.pl/pl/3-obuwie-meskie?selected_filters=page-1/rozmiar_obuwia-42-42_2_3-425-43-43_1_3-44-44_2_3-445-45-45_1_3-455-46-47')
#                 self.driver.get(url)
#                 time.sleep(3)
#               #  self.driver.refresh()
#                 page_source = self.driver.page_source
#                # print(self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML"))
#                 break
#             except:
#                 print("Connection refused by the server..")
#                 print("Let me sleep for 5 seconds")
#                 print("ZZzzzz...")
#                 print('Planet')
#                 time.sleep(5)
#                 print("Was a nice sleep, now let me continue...")
#                 continue
#
#         self.current_page = url
#
#         return page_source
#
#     def get_page_soup(self, url):
#         page_source = self.get_page_source(url)
#         soup = BeautifulSoup(page_source, 'html.parser')
#
#         return soup
#
#     def get_number_of_pages(self):
#         soup = self.get_page_soup(self.start_page_url)
#         #print(soup)
#
#         number_of_pages = int(soup.find(class_='pagination').find_all('li')[-2].find('span').text)
#         #print(number_of_pages)
#
#         return number_of_pages
#
#     def get_all_catalog_items(self, url):
#         soup = self.get_page_soup(url)
#         #print(soup)
#         catalog_items = soup.find_all(class_=re.compile('^ajax_block_product'))#.find_all(class_=' thumbnails product-container')
#         # print(catalog_items)
#         # print(len(catalog_items))
#         # print('scrapping')
#         return catalog_items[1:]
#
#     def get_sneaker_sizes(self, item_url):
#         soup = BeautifulSoup(self.get_page_source_fast(item_url), 'html.parser')
#         article = soup.find(class_='text-left small').text.split(' ')[-1]
#
#         # print(soup)
#         # print("#########################")
#        # print(article)
#
#         sizes = []
#         sizes_from_container = soup.find(class_='form-control attribute_select no-print').find_all('option')
#         # print(sizes_from_container)
#
#         for size in sizes_from_container:
#            # print(size['class'])
#             #if 'disabled' not in size['class']:
#                 sizes.append(size.text)
#
#        # time.sleep(0.5)
#
#         return article, sizes
#
#     def parse_catalog_items(self, url):
#         catalog_items = self.get_all_catalog_items(url)
#         sneakers = []
#
#         for item in catalog_items:
#             sneaker = []
#
#             sneaker_name = item.find(class_='caption').find(class_='text-center').find('span').text
#             sneaker_price = float(re.findall(r'\d+[,.]\d+', item.find(class_='price text-center').find('span').text.replace(',', '.'))[0])
#             sneaker_url = item.find('a')['href']
#             try:
#                 sneaker_article, sneaker_sizes = self.get_sneaker_sizes(sneaker_url)
#             except:
#                 continue
#             sneaker_article = sneaker_article.lower()
#
#             try:
#                 sneaker_brand = item.find(class_='caption').find('img')['alt']
#             except:
#                 sneaker_brand = 'Unknown'
#
#             try:
#                 sneaker_image_url = item.find('img')['src']
#             except:
#                 sneaker_image_url = 'No image'
#
#             print(sneaker_name)
#             print(sneaker_price)
#             print(sneaker_brand)
#             print(sneaker_image_url)
#
#             sneaker.append(sneaker_name)
#             sneaker.append(sneaker_price)
#             sneaker.append(sneaker_article)
#             sneaker.append(sneaker_url)
#             sneaker.append(sneaker_brand)
#             sneaker.append(sneaker_image_url)
#             sneaker.append(sneaker_sizes)
#
#             sneakers.append(sneaker)
#
#         return sneakers
#
#     def scrap(self):
#         pages_number = self.get_number_of_pages()
#         all_sneakers = []
#
#         for i in range(1, pages_number+1):
#         #for i in range(1, 1 + 1):
#             print(i)
#             url_to_scrap = self.page_pattern_url + str(i)
#             page_sneakers = self.parse_catalog_items(url_to_scrap)
#
#             for sneaker in page_sneakers:
#                 all_sneakers.append(sneaker)
#
#        # print(len(all_sneakers))
#         return all_sneakers



# planet = BasketPlanet()
# planet.scrap()


# sklep = SklepKoszykarza()
# print(sklep.scrap())
# sklep.driver.close()
