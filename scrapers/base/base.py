from abc import ABC, abstractmethod
from models.sneaker import Sneaker
from utils.driver import Driver


class BaseScraper(ABC):
    start_page_url = ''
    page_pattern_url = ''
    start_page_index = 0

    def __init__(self, existing_sneakers):
        self.driver = Driver()
        self.sneakers = existing_sneakers

    @abstractmethod
    def get_number_of_pages(self):
        pass

    @abstractmethod
    def get_all_page_item_containers(self, *args):
        pass

    @abstractmethod
    def get_sneaker_sizes(self, *args):
        pass

    @abstractmethod
    def get_sneaker_article(self, *args):
        pass

    @abstractmethod
    def get_sneaker_name(self, *args):
        pass

    @abstractmethod
    def get_sneaker_url(self, *args):
        pass

    @abstractmethod
    def get_sneaker_price(self, *args):
        pass

    @abstractmethod
    def get_sneaker_image_url(self, *args):
        pass

    def get_brand_name_from_item_name(self, item_name):
        brands = ['jordan', 'nike', 'adidas', 'under armour', 'ua']

        item_name = item_name.lower()

        for brand in brands:
            if brand in item_name:
                return brand

        return 'Unknown'

    def get_all_urls(self):
        all_urls = []
        number_of_pages = self.get_number_of_pages()
        last_page_index = number_of_pages + 1

        for page_number in range(self.start_page_index, last_page_index):
            all_urls.append('{}{}'.format(self.page_pattern_url, page_number))

        return all_urls

    def get_sneakers_from_page(self, url):
        item_containers = self.get_all_page_item_containers(url)
        #sneakers = {}

        for container in item_containers:
            #sneaker = []

            sneaker_name = self.get_sneaker_name(container)
            sneaker_price = self.get_sneaker_price(container)
            sneaker_url = self.get_sneaker_url(container)
            sneaker_article = self.get_sneaker_article(sneaker_url).lower()
            sneaker_sizes = self.get_sneaker_sizes(container)
            sneaker_brand = self.get_brand_name_from_item_name(sneaker_name)
            sneaker_image_url = self.get_sneaker_image_url(container)

            print(sneaker_name)
            print(sneaker_price)
            print(sneaker_brand)
            print(sneaker_image_url)

            sneaker = Sneaker(name=sneaker_name,
                              price=sneaker_price,
                              url=sneaker_url,
                              article=sneaker_article,
                              sizes=sneaker_sizes,
                              brand=sneaker_brand,
                              image_url=sneaker_image_url)

            try:
                _ = self.sneakers[sneaker_article]
                self.sneakers[sneaker_article].extend(sneaker)
            except KeyError as e:
                #print(e)
                self.sneakers[sneaker_article] = [sneaker]

            print(self.sneakers)

    def get_all_sneakers(self):
        all_urls = self.get_all_urls()
        print(all_urls)

        for url in all_urls:
            self.get_sneakers_from_page(url)

        return self.sneakers

