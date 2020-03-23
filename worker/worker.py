from scrapers.ataf.ataf import AtafScraper
from scrapers.sklepkoszykarza.sklepkoszykarza import SklepKoszykarzaScraper
from scrapers.basketplanet.basketplanet import BasketPlanetScraper
from scrapers.basketzone.basketzone import BasketZoneScraper
from scrapers.basketo.basketo import BaksetoScraper
from scrapers.basketmania.basketmania import BasketManiaScraper
from scrapers.adidas.adidas import AdidasScraper
from managers.scrapmanager import ScrapManager
from managers.imagemanager import ImageManager
from utils.dumpers import load_main_list


class Worker:
    def __init__(self):
        # scrap_manager = ScrapManager()
        # scrap_manager.add_scraper(AtafScraper)
        # scrap_manager.add_scraper(SklepKoszykarzaScraper)
        # scrap_manager.add_scraper(BasketPlanetScraper)
        # scrap_manager.add_scraper(BasketZoneScraper)
        # scrap_manager.add_scraper(BaksetoScraper)
        # scrap_manager.add_scraper(AdidasScraper)
        # scrap_manager.add_scraper(BasketManiaScraper)
        #
        # scrap_manager.scrap_all()
        ImageManager().download_images(load_main_list('parsed_sneakers.pickle'))
