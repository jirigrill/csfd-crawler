from bs4 import BeautifulSoup
from typing import Set, List
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class CSFDMainPageProcessor:
    def __init__(self, interested_sections: List[str]):
        self.interested_sections = interested_sections

    def extract_top_items_urls(self, html_page: BeautifulSoup) -> Set[str]:
        """
        Extract URLs of top items from specified sections on the main page.

        :param html_page(BeautifulSoup): The parsed HTML content of the main page.
        :return top_items_urls(Set[str]): A set of URLs for the top items.
        """
        top_items_urls = set()
        for h2 in html_page.find_all("h2"):
            section_title = h2.get_text(strip=True)
            if section_title in self.interested_sections:
                top_items = h2.parent.parent.find_all("a", href=True)
                top_items_urls.update(item["href"] for item in top_items)
        return top_items_urls

    @staticmethod
    def trim_episode_url_endpoint(url_end: str) -> str:
        """
        In case of tv show episode it removes the episode part from url_end.

        :param url_end(str): The end part of a URL.
        :return trimmed_url(str): The URL with the episode part removed.
        """
        return "/".join(url_end.split("/")[:3]) + "/"
