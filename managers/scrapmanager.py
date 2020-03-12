import pickle


# TODO:refactor using dictionaries instead of lists

class ScrapManager:
    """This class manages all existing scrapers,
    gets all products and then creates united
    list of products where every single item
    is unique and its primary key is equal to
    its article"""

    def __init__(self):
        self.scrapers = []
        self.all_items = []
        self.aritcle_based_lists = []
        self.main_list = []

    def add_scraper(self, scraper):
        self.scrapers.append(scraper)

    def get_all_items(self):
        for scraper in self.scrapers:
            sc = scraper()
            self.all_items.append([sc.scrap()])
            sc.driver.close()

    def get_articles_based_lists_of_items(self):
        for item in self.all_items:
            temp_list = []

            for sneaker in item:
                new_list_articles = []
                new_list_articles.append(sneaker[2])

                new_list_articles.append([sneaker])
                temp_list.append(new_list_articles)

            self.aritcle_based_lists.append(temp_list)

    def get_united_list(self):
        self.main_list.extend(self.aritcle_based_lists[0])

        for single_list in self.aritcle_based_lists:
            for i, element_i in enumerate(self.main_list):
                for j, element_j in enumerate(single_list):
                    if element_i[0] in element_j:
                        self.main_list[i][1].append(element_j[1][0])
                        single_list.remove(element_j)

            self.main_list.extend(single_list)

    def dump_main_list(self, file):
        with open('dumps/{}'.format(file), 'wb') as f:
            pickle.dump(self.main_list, f)
            f.close()

    def load_main_list(self, file):
        with open('dumps/{}'.format(file), 'rb') as f:
            self.main_list = pickle.load(f)
            f.close()

    def scrap_all(self):
        self.get_all_items()
        self.get_articles_based_lists_of_items()
        self.get_united_list()
        self.dump_main_list()

