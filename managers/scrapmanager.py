from utils.dumpers import dump_main_list


# TODO:refactor using dictionaries instead of lists

class ScrapManager:
    def __init__(self):
        self.scrapers = []
        self._all_items = {}

    def add_scraper(self, scraper):
        self.scrapers.append(scraper)

    def get_all_items(self):
        for scraper in self.scrapers:
            sc = scraper(self._all_items)
            self._all_items = sc.get_all_sneakers()
            sc.driver.firefox.close()

    def scrap_all(self):
        self.get_all_items()

        dump_main_list(file_name='parsed_sneakers.pickle',
                       data=self._all_items)

    @property
    def all_items(self):
        return self._all_items

    @all_items.setter
    def all_items(self, items):
        self._all_items = items
