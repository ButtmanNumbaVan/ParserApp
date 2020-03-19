import pickle


# TODO:refactor using dictionaries instead of lists

class ScrapManager:
    def __init__(self):
        self.scrapers = []
        self.all_items = {}

    def add_scraper(self, scraper):
        self.scrapers.append(scraper)

    def get_all_items(self):
        for scraper in self.scrapers:
            sc = scraper(self.all_items)
            self.all_items = sc.get_all_sneakers()
            sc.driver.firefox.close()


    def dump_main_list(self, file):
        with open('dumps/{}'.format(file), 'wb') as f:
            pickle.dump(self.all_items, f)
            f.close()

    def load_main_list(self, file):
        with open('dumps/{}'.format(file), 'rb') as f:
            self.all_items = pickle.load(f)
            f.close()

    def scrap_all(self):
        self.get_all_items()
       # self.dump_main_list

    def get_scraped_items(self):
        return self.all_items

