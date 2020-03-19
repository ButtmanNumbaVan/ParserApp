from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver import Firefox
from utils.requests.session import Session


class Driver:
    def __init__(self):
        self.firefox = Firefox()
        self.session = Session()

    def get_page_source_driver(self, url):
        page_source = ''
        while page_source == '':
            try:
                self.firefox.get(url)
                page_source = self.firefox.page_source
                break

            except:
                print("Connection refused by the server..")
                sleep(5)
                continue

        return page_source

    def get_page_source_session(self, url):
        page_source = ''
        while page_source == '':
            try:
                page_source = self.session.get(url, headers=self.session.headers)
                break

            except:
                print("Connection refused by the server..")
                sleep(5)
                continue

        return page_source.text

    def get_page_soup(self, url):
        page_source = self.get_page_source_driver(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup