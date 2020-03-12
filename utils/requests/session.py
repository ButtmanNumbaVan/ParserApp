from requests_html import HTMLSession
import requests


class Session(HTMLSession):
    def __init__(self):
        super().__init__()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                      ' Chrome/76.0.3809.132 Safari/537.36','Referer':'http://www.python.org/'}
        self.adapter = requests.adapters.HTTPAdapter(max_retries=10)
        self.mount('http://', self.adapter)