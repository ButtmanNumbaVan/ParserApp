from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver import Firefox
from utils.requests.session import Session
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

    def get_page_source_scroll_mania(self, url):
        page_source = ''
        while page_source == '':
            try:
                self.firefox.get(url)
                self.scroll_to_page_bottom()
                    # pass

                page_source = self.firefox.page_source
                break

            except:
                print("Connection refused by the server..")
                sleep(5)
                continue

        return page_source

    def scroll_to_page_bottom(self):
        """A method for scrolling the page."""

        # Get scroll height.
        last_height = self.firefox.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.firefox.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load the page.
            sleep(5)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.firefox.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    def get_page_source_scroll_adidas(self, url):
      #  page_source = ''
        while True:
            try:
                # driver = webdriver.Firefox()

                self.firefox.get(url)
                sleep(3)
                height = 100
                wait = WebDriverWait(self.firefox, 20)
                for _ in range(14):
                    height += 350
                    height_str = str(height)
                    js_function = "window.scrollTo(0, " + height_str + ")"
                    self.firefox.execute_script(js_function)
                    sleep(0.45)
                wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "gl-price__value")))
                print('here')
                # print(p_element.text)
                break
            except:
                print("Connection refused by the server..")
                print("Let me sleep for 5 seconds")
                print("ZZzzzz...")
                sleep(5)
                print("Was a nice sleep, now let me continue...")
                continue

        return self.firefox.page_source

    def get_page_soup(self, url):
        page_source = self.get_page_source_driver(url)
        soup = BeautifulSoup(page_source, 'html.parser')

        return soup