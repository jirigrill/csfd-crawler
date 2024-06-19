import bs4
import requests

from dataclasses import dataclass, field
from typing import List


@dataclass
class CSFDObject:
    type: str
    url: str
    name: str
    genre: List[str] = field(default_factory=list)
    rating: int = 0

    def __eq__(self, other):
        if not isinstance(other, CSFDObject):
            return False
        return (
            self.type == other.type
            and self.url == other.url
            and self.name == other.name
            and self.genre == other.genre  # Compare lists directly
            and self.rating == other.rating
        )

    def __hash__(self):
        # Convert mutable list to tuple to make it hashable
        genre_tuple = tuple(self.genre)
        return hash((self.type, self.url, self.name, genre_tuple, self.rating))


INTERESTED_SECTIONS = ["Nejnavštěvovanější seriály", "Nejnavštěvovanější filmy"]
BASE_URL = "https://www.csfd.cz"
HEADERS = {"User-agent": "csfd crawler"}


def fetch_page(url: str, headers: dict) -> bs4:
    """Fetch the page content from a given URL."""
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an error for bad status codes
    return bs4.BeautifulSoup(response.text, features="html.parser")


def extract_top_items_urls(html_page: bs4, sections: list) -> set:
    """Extract URLs of top items from specified sections on the main page."""
    top_items_urls = set()
    for h2 in html_page.find_all("h2"):
        section_title = h2.get_text(strip=True)
        if section_title in sections:
            top_items = h2.parent.parent.find_all("a", href=True)
            for item in top_items:
                top_items_urls.add(item["href"])
    return top_items_urls


def extract_type(html_page: bs4) -> str:
    """Extracts type (tvshow/movie) from item's page."""
    try:
        html_page.find("div", {"class": "film-header-name"}).find(
            "span", {"class": "type"}
        ).get_text(strip=True)
        return "tvshow"
    except AttributeError:
        return "movie"


def extract_us_title(html_page: bs4) -> str:
    """Extract US title from an item's page."""
    titles = html_page.find("ul", {"class": "film-names"})

    if titles:
        for title in titles.find_all("li"):
            us_flag = title.find("img", {"title": "USA"})
            if us_flag:
                # filters out "Pracovni nazev" version of titles
                if us_flag.parent.find("span", class_="info") is None:
                    return us_flag.parent.get_text(strip=True).replace("(více)", "")
    else:
        title_div = html_page.find("div", {"class": "film-header-name"})
        if title_div and title_div.h1:
            return title_div.h1.get_text(strip=True)


def trim_episode_url_endpoint(url_end: str) -> str:
    """In case of tv show episode it removes the episode part from url_end"""
    parts = url_end.split("/")
    return "/".join(parts[:3]) + "/"


def extract_genre(html_page: bs4) -> str:
    genres = html_page.find("div", {"class": "genres"})
    genres_list = []
    for genre in genres:
        genre = genre.get_text(strip=True).replace("/", "").replace(" ", "")
        if genre != "":
            genres_list.append(genre)
    return genres_list


def extract_rating(html_page: bs4) -> int:
    try:
        return int(
            html_page.find("div", {"class": "film-rating-average"})
            .get_text(strip=True)
            .replace("%", "")
        )
    except ValueError:
        return 0


def main():
    main_page = fetch_page(BASE_URL, HEADERS)
    top_items_urls = extract_top_items_urls(main_page, INTERESTED_SECTIONS)

    csfd_objects = set()
    for url_end in top_items_urls:
        item_url = f"{BASE_URL}{trim_episode_url_endpoint(url_end)}"
        item_html = fetch_page(item_url, HEADERS)
        item_type = extract_type(item_html)
        item_us_title = extract_us_title(item_html)
        item_genre = extract_genre(item_html)
        item_rating = extract_rating(item_html)
        if item_us_title is not None:
            csfd_objects.add(
                CSFDObject(
                    type=item_type,
                    url=item_url,
                    name=item_us_title,
                    genre=item_genre,
                    rating=item_rating,
                )
            )
        else:
            print(f"'{item_url}' has not us title.")
    print("The most visited URLs scraped.")


if __name__ == "__main__":
    main()
