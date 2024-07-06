from bs4 import BeautifulSoup
from typing import Set, List, Optional
import requests
import logging

from .csfd_object import CSFDObject
from .csfd_main_page_processor import CSFDMainPageProcessor
from .csfd_item_parser import CSFDItemParser

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class WebScraper:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers

    def _fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch the page content from a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, features="html.parser")
        except requests.RequestException as e:
            logger.error("Failed to fetch page %s: %s", url, e)
            return None

class CSFDScraper(WebScraper):
    def __init__(self, base_url: str, headers: dict, interested_sections: List[str]):
        super().__init__(base_url, headers)
        self.page_processor = CSFDMainPageProcessor(interested_sections)

    def scrape(self) -> Set[CSFDObject]:
        main_page = self._fetch_page(self.base_url)
        if not main_page:
            logger.error("Failed to fetch main page. Exiting.")
            return set()

        top_items_urls = self.page_processor.extract_top_items_urls(main_page)
        csfd_objects = set()

        for url_end in top_items_urls:
            item_url = f"{self.base_url}{self.page_processor.trim_episode_url_endpoint(url_end)}"
            item_html = self._fetch_page(item_url)
            if item_html:
                parser = CSFDItemParser(item_html, item_url)
                csfd_object = parser.parse_item()
                if csfd_object:
                    csfd_objects.add(csfd_object)

        logger.info("Scraped %d items.", len(csfd_objects))
        for obj in csfd_objects:
            logger.info("Scraped: %s (%d) - %s", obj.name, obj.year, obj.type)

        return csfd_objects