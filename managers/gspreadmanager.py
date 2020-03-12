from utils.spreadsheets.googlespreadsheet import SpreadSheet
import time


class GSpreadManager:
    def __init__(self, sneakers_list):
        self.spread_sheet = SpreadSheet()
        self.sneakers_list = sneakers_list

        self.start_index_rows_range = 0
        self.last_sneakers_number = 0
        self.names = []
        self.articles = []
        self.prices = []
        self.sneaker_sizes = []
        self.sneaker_urls = []
        self.sneaker_brands = []
        self.sneaker_image_urls = []

    def merge_cells(self):
        for i, sneaker in enumerate(self.sneakers_list):
            sneakers_number = len(sneaker[1])
            print(sneaker[1])
            print(sneaker)
            print(sneakers_number)

            self.start_index_rows_range += self.last_sneakers_number
            end_index_rows_range = self.start_index_rows_range + sneakers_number

            self.last_sneakers_number = sneakers_number

            if sneakers_number > 1:
                # while True:
                # try:
                merged = False
                while not merged:
                    try:
                        self.spread_sheet.merge_cells((self.start_index_rows_range, end_index_rows_range), 4)
                        time.sleep(1.1)
                        merged = True
                    except Exception as e:
                        time.sleep(101)

    def get_all_needed_data(self):
        for i, sneaker in enumerate(self.sneakers_list):
            for j, item in enumerate(sneaker[1]):
                price = item[1], url = item[3], article = item[2]
                name = item[0], brand = item[4], image = item[5]

                sizes = str(item[-1])

                self.prices.append(price)
                self.sneaker_sizes.append(sizes)
                self.articles.append(article)
                self.names.append(name)
                self.sneaker_urls.append(url)
                self.sneaker_brands.append(brand)
                self.sneaker_image_urls.append(image)

    #TODO:refactor
    def populate_sheet(self):
        self.merge_cells()
        self.get_all_needed_data()

        sneakers_len = str(sum(len(item[1]) for item in self.sneakers_list))
        cell_list_names = self.spread_sheet.sheet.range('A1:A{}'.format(sneakers_len))

        for i, val in enumerate(self.names):
            cell_list_names[i].value = val

        self.spread_sheet.sheet.update_cells(cell_list_names)
        time.sleep(1)
        ##################################################################################
        cell_list_articles = self.spread_sheet.sheet.range('B1:B{}'.format(sneakers_len))
        for i, val in enumerate(self.articles):
            cell_list_articles[i].value = val

        self.spread_sheet.sheet.update_cells(cell_list_articles)
        time.sleep(1)
        ##################################################################################
        cell_list_brands = self.spread_sheet.sheet.range('C1:C{}'.format(sneakers_len))
        for i, val in enumerate(self.sneaker_brands):
            cell_list_brands[i].value = val

        self.spread_sheet.sheet.update_cells(cell_list_brands)
        #################################################################################
        cell_list_images = self.spread_sheet.sheet.range('D1:D{}'.format(sneakers_len))
        for i, val in enumerate(self.sneaker_image_urls):
            formula = '=image("{}")'.format(val)
            cell_list_images[i].value = formula

        self.spread_sheet.sheet.update_cells(cell_list_images, value_input_option='USER_ENTERED')
        #################################################################################
        cell_list_prices = self.spread_sheet.sheet.range('E1:E{}'.format(sneakers_len))
        for i, val in enumerate(self.prices):
            cell_list_prices[i].value = str(val)

        self.spread_sheet.sheet.update_cells(cell_list_prices)
        time.sleep(1)
        ##################################################################################
        cell_list_urls = self.spread_sheet.sheet.range('F1:F{}'.format(sneakers_len))
        for i, val in enumerate(self.sneaker_urls):
            cell_list_urls[i].value = val

        self.spread_sheet.sheet.update_cells(cell_list_urls)
        ##################################################################################
        cell_list_sizes = self.spread_sheet.sheet.range('G1:G{}'.format(sneakers_len))
        for i, val in enumerate(self.sneaker_sizes):
            cell_list_sizes[i].value = val

        self.spread_sheet.sheet.update_cells(cell_list_sizes)


