from bs4 import BeautifulSoup
from typing import List, Optional
import logging
import re

from .csfd_object import CSFDObject


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class CSFDItemParser:
    def __init__(self, html_page: BeautifulSoup, url: str):
        self.html_page = html_page
        self.url = url

    def parse_item(self) -> Optional[CSFDObject]:
        item_type = self._extract_type()
        item_us_title = self._extract_us_title()
        if not item_us_title:
            logger.warning("'%s' has no US title.", self.url)
            return None

        return CSFDObject(
            type=item_type,
            url=self.url,
            name=item_us_title,
            year=self._extract_year(item_type),
            genre=self._extract_genre(),
            rating=self._extract_rating()
        )

    def _extract_type(self) -> str:
        """Extracts type (tvshow/movie) from item's page."""
        type_span = self.html_page.find("div", {"class": "film-header-name"})
        if type_span and type_span.find("span", {"class": "type"}):
            return "tvshow"
        return "movie"

    def _extract_us_title(self) -> Optional[str]:
        """Extract US title from an item's page."""
        titles = self.html_page.find("ul", {"class": "film-names"})
        if titles:
            for title in titles.find_all("li"):
                us_flag = title.find("img", {"title": "USA"})
                if us_flag and not us_flag.parent.find("span", class_="info"):
                    return us_flag.parent.get_text(strip=True).replace("(více)", "").replace("(méně)", "")
        else:
            title_div = self.html_page.find("div", {"class": "film-header-name"})
            if title_div and title_div.h1:
                return title_div.h1.get_text(strip=True)
        return None

    def _extract_genre(self) -> List[str]:
        genres = self.html_page.find("div", {"class": "genres"})
        return [genre.get_text(strip=True).replace("/", "").replace(" ", "") 
                for genre in genres if genre.get_text(strip=True)]

    def _extract_rating(self) -> int:
        rating_div = self.html_page.find("div", {"class": "film-rating-average"})
        if rating_div:
            try:
                return int(rating_div.get_text(strip=True).replace("%", ""))
            except ValueError:
                logger.warning("Failed to parse rating")
        return 0

    def _extract_year(self, item_type: str) -> int:
        origin_div = self.html_page.find("div", {"class": "origin"})
        if origin_div and origin_div.find("span"):
            year_text = origin_div.find("span").get_text(strip=True).replace(",", "")
            if item_type == "tvshow":
                match = re.search(r"\b(\d{4})\b", year_text)
                if match:
                    return int(match.group(1))
            else:
                try:
                    return int(year_text)
                except ValueError:
                    logger.warning("Failed to parse year: %s", year_text)
        return 0