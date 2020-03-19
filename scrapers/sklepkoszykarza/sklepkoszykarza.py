import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from scrapers.base.base import BaseScraper
import time


class SklepKoszykarzaScraper(BaseScraper):
    start_page_url = 'https://sklepkoszykarza.pl/products/obuwie/category,2/item,72/page,1'
    page_pattern_url = 'https://sklepkoszykarza.pl/products/obuwie/category,2/item,72/page,'
    start_page_index = 1

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)

    def get_number_of_pages(self):
        soup = self.driver.get_page_soup(self.start_page_url)

        number_of_pages = int(soup.find(class_='pagination__input').find('span').text[-1])
        print(number_of_pages)

        return number_of_pages

    def get_all_page_item_containers(self, url):
        soup = self.driver.get_page_soup(url)
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

    def get_sneaker_article(self, item):
        return item.find(class_='s').find('span').text.lower()

    def get_sneaker_name(self, container):
        return container.find(class_='n').text.replace('\n', "")

    def get_sneaker_price(self, container):
        return float(re.findall(r'\d+[,.]\d+', container.find(class_='ps pricebox').text.replace(',', '.'))[0])

    def get_sneaker_url(self, container):
        return container.find('a')['href']

    def get_sneaker_image_url(self, container):
        try:
            sneaker_image_url = container.find('img')['data-echo']
        except:
            try:
                sneaker_image_url = container.find('img')['src']
            except:
                sneaker_image_url = 'No image'

        return sneaker_image_url
