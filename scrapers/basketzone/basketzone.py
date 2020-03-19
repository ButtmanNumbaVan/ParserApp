import requests
import re
from requests_html import HTMLSession
from selenium import webdriver
from bs4 import BeautifulSoup
from scrapers.base.base import BaseScraper
from utils.requests.session import Session
import time


class BasketZoneScraper(BaseScraper):
    start_page_url = 'https://basketzone.pl/index.php?action=przegladaj&kat=3&partia=0'
    page_pattern_url = 'https://basketzone.pl/index.php?action=przegladaj&kat=3&partia='
    start_page_index = 0

    def __init__(self, existing_sneakers):
        super().__init__(existing_sneakers)

    def get_number_of_pages(self):
        soup = self.driver.get_page_soup(self.start_page_url)

        number_of_pages = int(soup.find(class_='pages').find_all('span')[-1].find('a')['href'][-2:])
        print(number_of_pages)

        return number_of_pages

    def get_all_page_item_containers(self, url):
        soup = self.driver.get_page_soup(url)
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

    def get_sneaker_article(self, item_url):
        soup = BeautifulSoup(self.driver.get_page_source_session(item_url), 'html.parser')
        article = soup.find(class_='product-page-indeks').text.replace(" ", "").replace("\n", "")

        return article.lower()

    def get_sneaker_name(self, container):
        return container.find(class_='name').text.replace("\n", "")

    def get_sneaker_price(self, container):
        return float(re.findall(r'\d+[,.]\d+', container.find(class_='prices clearfix').find_all('span')[-2].
                                text.replace(',', '.'))[0])

    def get_sneaker_url(self, container):
        return container.find('a')['href']

    def get_sneaker_image_url(self, container):
        try:
            sneaker_image_url = container.find('img')['src']
        except:
            sneaker_image_url = 'No image'

        return sneaker_image_url



# zone = BasketZone()
# zone.scrap()

# sklep = SklepKoszykarza()
# print(sklep.scrap())
# sklep.driver.close()
