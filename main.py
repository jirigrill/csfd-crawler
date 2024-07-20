import logging
from src.config import Config
from src.web_scraper import CSFDScraper

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


def main() -> None:
    scraper = CSFDScraper(Config.BASE_URL, Config.HEADERS, Config.INTERESTED_SECTIONS)
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
