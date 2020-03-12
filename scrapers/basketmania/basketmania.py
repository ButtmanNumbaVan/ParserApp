from selenium import webdriver
from bs4 import BeautifulSoup
from utils.requests.session import Session
#from utils.spreadsheets.googlespreadsheet import SpreadSheet
#from parsers.sklepkoszykarza.sneakersgetter import SklepKoszykarza
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


class BasketMania:
    def __init__(self):
        self.session = Session()
        self.start_page_url = 'https://www.ataf.pl/854-buty-do-koszykowki?&page=1'
        self.page_pattern_url = 'https://basketmania.pl/pol_m_Buty-149.html'
        self.item_patter_url = 'https://basketmania.pl'
        self.start_page_index = 1
        self.current_page_url = self.start_page_url
        self.driver = webdriver.Firefox()

    def get_page_source(self, url, scroll=False):
        page_source = ''
        while page_source == '':
            try:
                self.driver.get(url)

                if scroll:
                    self.scroll_to_page_bottom()
                    #pass

                page_source = self.driver.page_source
                break

            except:
                print("Connection refused by the server..")
                time.sleep(5)
                continue

        return page_source

    def get_page_source_fast(self, url):
        page_source = ''
       # print(url)
        while page_source == '':
            try:
                page_source = self.session.get(url, headers = self.session.headers)
                break

            except:
                print("Connection refused by the server..1")
                time.sleep(5)
                continue

        return page_source.text

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
        catalog_items = soup.find(class_='main_hotspot').find_all(class_=re.compile("^product_wrapper"))

        return catalog_items

    def scroll_to_page_bottom(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            time.sleep(5)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def get_article(self, item_url):
        soup = BeautifulSoup(self.get_page_source(item_url), 'html.parser')
        try:
            article = soup.find(string="Kod produktu: ").find_next('strong').contents[0]
        except:
            article = 'None'

       # print(soup)
       # print("#########################")
       # print(article)

        sizes = []
        sizes_from_container = soup.find(class_='fsp_eur').find_all(class_=re.compile("^fsp_element"))
        #print(sizes_from_container)

        for size in sizes_from_container:
            #print(size['class'])
            if 'disabled' not in size['class']:
                sizes.append(size.text)

        return article, sizes

    def parse_catalog_items(self, url):
        catalog_items = self.get_all_catalog_items(url)
        sneakers = []

        for item in catalog_items:
            sneaker = []

            sneaker_name = item.find(class_='product-name').text
            #print(sneaker_name)
            sneaker_price = float(re.findall(r'\d+[,.]\d+', item.find(class_='price').text.replace(',', '.'))[0])
            sneaker_url = self.item_patter_url + item.find('a')['href']
           # print(sneaker_url + ' here')
            try:
                sneaker_article, sneaker_sizes = self.get_article(sneaker_url)
            except:
                continue
            sneaker_article = sneaker_article.lower()
            print(sneaker_article)
            print(sneaker_name)

            try:
                sneaker_brand = item.find(class_='firm-name').find('a').text
            except:
                sneaker_brand = 'Unknown'

            try:
                sneaker_image_url = self.item_patter_url + item.find('img')['data-src']
            except:
                sneaker_image_url = 'No image'
            #print(sneaker_article)
           # print(sneaker_sizes)

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
        #print(sneakers)
        return sneakers

    def scrap(self):
        #pages_number = self.get_number_of_pages()
        all_sneakers = []

        url_to_scrap = self.page_pattern_url

        page_sneakers = self.parse_catalog_items(url_to_scrap)

        for sneaker in page_sneakers:
            all_sneakers.append(sneaker)

        return all_sneakers

# mania = BasketMania()
# mania.scrap()