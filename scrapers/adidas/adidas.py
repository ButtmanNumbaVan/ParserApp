import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from scrapers.base.base import BaseScraper
from utils.decorators import error_catcher
import time


class AdidasScraper(BaseScraper):
    item_patter_url = 'https://www.adidas.pl'

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)

    def get_all_urls(self):
        return ['https://www.adidas.pl/mezczyzni-buty-koszykowka?start=0',
                'https://www.adidas.pl/mezczyzni-buty-koszykowka?start=48']

    def get_page_soup(self, url):
        page_source = self.driver.get_page_source_scroll_adidas(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    def get_number_of_pages(self):
        super().get_number_of_pages()

    def get_all_page_item_containers(self, url):
        soup = self.get_page_soup(url)
        #print(soup)
        catalog_items = soup.find_all(class_=re.compile('^gl-product-card glass-product-card'))
        print(len(catalog_items))
        print(catalog_items)
        return catalog_items

    @error_catcher
    def get_sneaker_article(self, container):
        url = self.get_sneaker_url(container)
        source = self.driver.get_page_source_driver(url)
        time.sleep(4.5)

        soup = BeautifulSoup(self.driver.firefox.page_source, 'html.parser')
        article = soup.find(string=re.compile("^Kod produktu")).split(' ')[-1]

        return article

    @error_catcher
    def get_sneaker_sizes(self, container):
        soup = BeautifulSoup(self.driver.firefox.page_source, 'html.parser')

        sizes = []
        sizes_from_container = soup.find(class_='square-list').find_all('button')
        # print(sizes_from_container)

        for size in sizes_from_container:
            sizes.append(size.text)

        return sizes

    @error_catcher
    def get_sneaker_name(self, container):
        return container.find(class_='gl-product-card__details-main').\
            find(class_=re.compile('^gl-product-card__name')).text

    @error_catcher
    def get_sneaker_price(self, container):
        #print('price{}'.format(container.find(text=re.compile(r'^\d+[\s]zł$'))))
        sneaker_price = re.findall(r'\d+',
                                   container.find(text=re.compile(r'^\d+[\s]zł$')))

        return float(sneaker_price[0])

    @error_catcher
    def get_sneaker_url(self, container):
        return self.item_patter_url + container.find(class_='gl-product-card__details').find('a')['href']

    @error_catcher
    def get_sneaker_image_url(self, container):
        sneaker_image_url = container.find('img')['src']

        return sneaker_image_url

    def get_brand_name_from_item_name(self, container):
        return 'adidas'


# adidas = Adidas()
# adidas.scrap()