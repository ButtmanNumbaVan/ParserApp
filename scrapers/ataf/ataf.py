from selenium import webdriver
from bs4 import BeautifulSoup
from utils.requests.session import Session
from scrapers.base.base import BaseScraper
from models.sneaker import Sneaker
import time
import re

import pickle
import requests


class AtafScraper(BaseScraper):
    start_page_url = 'https://www.ataf.pl/854-buty-do-koszykowki?&page=1'
    page_pattern_url = 'https://www.ataf.pl/854-buty-do-koszykowki?&page='
    start_page_index = 1

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)

    def get_number_of_pages(self):
       #  soup = self.get_page_soup(self.start_page_url)
       #
       #  number_of_pages = int(soup.find(class_='pagination__input').find('span').text[-1])
       # # print(number_of_pages)

        return 6

    def get_all_page_item_containers(self, url):
        soup = self.driver.get_page_soup(url)
        item_containers = soup.find(class_='pcajax row').find_all(class_='col-md-6 col-lg-4 no-pad')

        return item_containers

    def get_sneaker_sizes(self, item):
        sizes = []
        sizes_from_container = item.find_all('span')

        for size in sizes_from_container:
            sizes.append(size.text[3:])

        return sizes

    def get_sneaker_article(self, item_url):
        soup = BeautifulSoup(self.driver.get_page_source_session(item_url), 'html.parser')
        article = soup.find(string="Kod produktu:").find_next('td').contents[0]

        return article.lower()

    def get_sneaker_name(self, container):
        return container.find(class_='slider-product').text

    def get_sneaker_price(self, container):
        return float(re.findall(r'\d+[,.]\d+', container.find(class_='slider-price').text.replace(',', '.'))[0])

    def get_sneaker_url(self, container):
        return container.find('a')['href']

    def get_sneaker_image_url(self, container):
        try:
            sneaker_image_url = container.find('img')['src']
        except:
            sneaker_image_url = 'No image'

        return sneaker_image_url

    # def get_sneakers_from_page(self, url):
    #     item_containers = self.get_all_page_item_containers(url)
    #     #sneakers = {}
    #
    #     for container in item_containers:
    #         #sneaker = []
    #
    #         sneaker_name = self.get_sneaker_name(container)
    #         sneaker_price = self.get_sneaker_price(container)
    #         sneaker_url = self.get_sneaker_url(container)
    #         sneaker_article = self.get_sneaker_article(sneaker_url)
    #         sneaker_sizes = self.get_sneaker_sizes(container)
    #         sneaker_brand = self.get_brand_name_from_item_name(sneaker_name)
    #         sneaker_image_url = self.get_sneaker_image_url(container)
    #
    #         print(sneaker_name)
    #         print(sneaker_price)
    #         print(sneaker_brand)
    #         print(sneaker_image_url)
    #
    #         sneaker = Sneaker(name=sneaker_name,
    #                           price=sneaker_price,
    #                           url=sneaker_url,
    #                           article=sneaker_article,
    #                           sizes=sneaker_sizes,
    #                           brand=sneaker_brand,
    #                           image_url=sneaker_image_url)
    #
    #         # sneaker.append(sneaker_name)
    #         # sneaker.append(sneaker_price)
    #         # sneaker.append(sneaker_article)
    #         # sneaker.append(sneaker_url)
    #         # sneaker.append(sneaker_brand)
    #         # sneaker.append(sneaker_image_url)
    #         # sneaker.append(sneaker_sizes)
    #
    #         if self.sneakers[sneaker_article]:
    #             self.sneakers[sneaker_article].extend(sneaker)
    #         else:
    #             self.sneakers[sneaker_article] = [sneaker]
    #
    #     #return sneakers
    #
    # def get_all_sneakers(self):
    #     all_urls = self.get_all_urls()
    #
    #     for url in all_urls:
    #     #for page_number in range(1, 1 + 1):
    #         #url_to_scrap = self.page_pattern_url + str(page_number)
    #         #print(url_to_scrap)
    #         self.get_sneakers_from_page(url)
    #
    #    # return all_sneakers