import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from scrapers.base.base import BaseScraper
from utils.decorators import error_catcher
import time


class BaksetoScraper(BaseScraper):
    start_page_url = 'https://basketo.pl/pol_m_Obuwie_Buty-do-koszykowki-227.html'
    page_pattern_url = 'https://basketo.pl/pol_m_Obuwie_Buty-do-koszykowki-227.html?counter='
    item_pattern_url = 'https://basketo.pl'
    start_page_index = 0

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)
    # def __init__(self):
    #    # self.session = Session()
    #     self.start_page_url = 'https://basketo.pl/pol_m_Obuwie_Buty-do-koszykowki-227.html#180'
    #     self.page_pattern_url = 'https://basketo.pl/pol_m_Obuwie_Buty-do-koszykowki-227.html#180'
    #     self.start_page_index = 1
    #     self.current_page_url = self.start_page_url
    #     self.driver = webdriver.Firefox()
    #     #self.all_sneakers = []

    def get_number_of_pages(self):
        soup = self.driver.get_page_soup(self.start_page_url)

        number_of_pages = int(soup.find(class_='s_paging__item pagination mb-2 mb-sm-3').find_all('li')[-2].text)
       # print(number_of_pages)

        return number_of_pages

    def get_all_page_item_containers(self, url):
        soup = self.driver.get_page_soup(url)
       # print(soup)
        catalog_items = soup.find_all(class_='product col-12 col-sm-4 col-md-3 pt-3 pb-md-3 mb-3 mb-sm-0')
        #print(len(catalog_items))
        return catalog_items

    @error_catcher
    def get_sneaker_sizes(self, item):
        sizes = []
        sizes_from_container = item.find(class_='product__sizes mb-1').find_all('span')
        #print(sizes_from_container)

        for size in sizes_from_container:
            sizes.append(size.text)

        return sizes

    @error_catcher
    def get_sneaker_article(self, container):
        return container.find(class_='product__name').text.split(' ')[-1].lower()

    @error_catcher
    def get_sneaker_name(self, container):
        return container.find(class_='product__name').text

    @error_catcher
    def get_sneaker_price(self, container):
        return float(re.findall(r'\d+[,.]\d+', container.find(class_='price').text.replace(',', '.'))[0])

    @error_catcher
    def get_sneaker_url(self, container):
        return self.item_pattern_url + container.find(class_='product__name')['href']

    @error_catcher
    def get_sneaker_image_url(self, container):
        image = container.find('img')
       # print(image.attrs.keys())
        if 'data-src' in image.attrs.keys():
            sneaker_image_url = self.item_pattern_url + container.find('img')['data-src']
        elif 'src' in image.attrs.keys():
            sneaker_image_url = self.item_pattern_url + container.find('img')['src']
        else:
            sneaker_image_url = 'No image'

        return sneaker_image_url



# basketo = SklepKoszykarza()
# basketo.scrap()

# sklep = SklepKoszykarza()
# print(sklep.scrap())
# sklep.driver.close()
