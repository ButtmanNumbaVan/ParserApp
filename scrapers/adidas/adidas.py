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


class Adidas:
    def __init__(self):
        self.session = Session()
        #self.start_page_url = 'https://sklepkoszykarza.pl/products/obuwie/category,2/item,72/page,1'
        #self.page_pattern_url = 'https://sklepkoszykarza.pl/products/obuwie/category,2/item,72/page,'
        self.pages_urls = ['https://www.adidas.pl/mezczyzni-buty-koszykowka?start=0',
                           'https://www.adidas.pl/mezczyzni-buty-koszykowka?start=48']
        self.start_page_index = 1
        #self.current_page_url = self.start_page_url
        self.driver = webdriver.Firefox()
        #self.all_sneakers = []

    def get_page_source_fast(self, url):
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
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        self.current_page = url

        return page_source

    def get_page_source_scroll(self, url):
      #  page_source = ''
        while True:
            try:
                # driver = webdriver.Firefox()

                self.driver.get(url)
                time.sleep(3)
                height = 100
                wait = WebDriverWait(self.driver, 20)
                for _ in range(14):
                    height += 350
                    height_str = str(height)
                    js_function = "window.scrollTo(0, " + height_str + ")"
                    self.driver.execute_script(js_function)
                    time.sleep(0.45)
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "gl-price__value")))
                print('here')
                # print(p_element.text)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                time.sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        return self.driver.page_source

    def get_page_soup(self, url):
        page_source = self.get_page_source_scroll(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup

    # def get_number_of_pages(self):
    #     soup = self.get_page_soup(self.start_page_url)
    #
    #     number_of_pages = int(soup.find(class_='pagination__input').find('span').text[-1])
    #     print(number_of_pages)
    #
    #     return number_of_pages

    def get_all_catalog_items(self, url):
        soup = self.get_page_soup(url)
        #print(soup)
        catalog_items = soup.find_all(class_=re.compile('^gl-product-card glass-product-card'))
        print(len(catalog_items))
        print(catalog_items)
        return catalog_items

    def get_article(self, item_url):
        source = self.get_page_source_fast(item_url)
        time.sleep(4.5)

        # wait = WebDriverWait(self.driver, 3)
        # wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "square-list")))

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        article = soup.find(string=re.compile("^Kod produktu")).split(' ')[-1]

       # print(soup)
       # print("#########################")
       # print(article)

        sizes = []
        sizes_from_container = soup.find(class_='square-list').find_all('button')
        #print(sizes_from_container)

        for size in sizes_from_container:
            #print(size['class'])
           # if 'disabled' not in size['class']:
                sizes.append(size.text)

        return article, sizes

    def parse_catalog_items(self, url):
        catalog_items = self.get_all_catalog_items(url)
        sneakers = []

        for item in catalog_items:
            sneaker = []
            sneaker_name = item.find(class_='gl-product-card__details-main').find(class_=re.compile('^gl-product-card__name')).text
            try:
                sneaker_price = float(re.findall(r'\d+[,.\d]\d+', item.find(class_='gl-product-card__details-main').find('span').text.replace(" ", "").replace(',', '.'))[0])
            except Exception as e:
                print(e, ' price')
                sneaker_price = 0
            #sneaker_price = item.find(class_='gl-product-card__details-main').find('span').text
            #sneaker_article = item.find(class_='s').find('span').text.lower()
            sneaker_url = 'https://www.adidas.pl' + item.find(class_='gl-product-card__details').find('a')['href']
            sneaker_brand = 'adidas'
            try:
                sneaker_article, sneaker_sizes = self.get_article(sneaker_url)
            except:
                print('Exception')
                continue
            sneaker_article = sneaker_article.lower()

            try:
                sneaker_image_url = item.find('img')['src']
            except Exception as e:
                print(e, ' image')
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
       # pages_number = self.get_number_of_pages()
        all_sneakers = []

        for url in self.pages_urls:
            url_to_scrap = url
            page_sneakers = self.parse_catalog_items(url_to_scrap)

            for sneaker in page_sneakers:
                all_sneakers.append(sneaker)

       # print(len(all_sneakers))
        return all_sneakers

# adidas = Adidas()
# adidas.scrap()