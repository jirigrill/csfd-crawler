import logging

from src.web_scraper import CSFDScraper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    BASE_URL = "https://www.csfd.cz"
    HEADERS = {"User-agent": "csfd crawler"}
    INTERESTED_SECTIONS = ["Nejnavštěvovanější seriály", "Nejnavštěvovanější filmy"]

    scraper = CSFDScraper(BASE_URL, HEADERS, INTERESTED_SECTIONS)
    results = scraper.scrape()

    for item in results:
        print(f"Title: {item.name}")
        print(f"Type: {item.type}")
        print(f"Year: {item.year}")
        print(f"Genres: {', '.join(item.genre)}")
        print(f"Rating: {item.rating}%")
        print("---")


if __name__ == "__main__":
    main()
