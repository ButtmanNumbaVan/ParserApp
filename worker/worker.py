from scrapers.adidas.adidas import Adidas
from scrapers.ataf.ataf import Ataf
from scrapers.sklepkoszykarza.sklepkoszykarza import SklepKoszykarza
from scrapers.basketplanet.basketplanet import BasketPlanetScraper
from scrapers.basketzone.basketzone import BasketZone
from scrapers.basketo.basketo import Bakseto
from managers.scrapmanager import ScrapManager


class Worker:
    def __init__(self):
        scrap_manager = ScrapManager()
        scrap_manager.add_scraper(Ataf)
        scrap_manager.add_scraper(SklepKoszykarza)
        scrap_manager.add_scraper(BasketPlanetScraper)
        scrap_manager.add_scraper(BasketZone)
        scrap_manager.add_scraper(Bakseto)

        scrap_manager.scrap_all()