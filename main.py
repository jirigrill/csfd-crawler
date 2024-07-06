import bs4
import requests
import re
import logging

from src.web_scrapper import CSFDScraper

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)


def main() -> None:
    BASE_URL = "https://www.csfd.cz"
    HEADERS = {"User-agent": "csfd crawler"}
    INTERESTED_SECTIONS = ["Nejnavštěvovanější seriály", "Nejnavštěvovanější filmy"]

    scraper = CSFDScraper(BASE_URL, HEADERS, INTERESTED_SECTIONS)
    scraper.scrape()


if __name__ == "__main__":
    main()
