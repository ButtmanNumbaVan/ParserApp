from scrapers.adidas.adidas import Adidas
from scrapers.ataf.ataf import AtafScraper
from scrapers.sklepkoszykarza.sklepkoszykarza import SklepKoszykarzaScraper
from scrapers.basketplanet.basketplanet import BasketPlanetScraper
from scrapers.basketzone.basketzone import BasketZoneScraper
from scrapers.basketo.basketo import Bakseto
from managers.scrapmanager import ScrapManager


class Worker:
    def __init__(self):
        scrap_manager = ScrapManager()
        scrap_manager.add_scraper(AtafScraper)
        scrap_manager.add_scraper(SklepKoszykarzaScraper)
        #scrap_manager.add_scraper(BasketPlanetScraper)
        #scrap_manager.add_scraper(BasketZoneScraper)
        #scrap_manager.add_scraper(Bakseto)

        scrap_manager.scrap_all()