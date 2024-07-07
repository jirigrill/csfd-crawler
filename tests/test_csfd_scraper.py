import pytest
from unittest.mock import patch

from src.web_scraper import CSFDScraper
from src.csfd_object import CSFDObject


class TestCSFDScraper:
    @pytest.fixture
    def csfd_scraper(self, base_url, headers):
        return CSFDScraper(base_url, headers, ["Test Section"])

    @patch("src.web_scraper.WebScraper._fetch_page")
    @patch("src.csfd_main_page_processor.CSFDMainPageProcessor.extract_top_items_urls")
    @patch("src.csfd_item_parser.CSFDItemParser.parse_item")
    def test_scrape(
        self,
        mock_parse_item,
        mock_extract_urls,
        mock_fetch_page,
        csfd_scraper,
        sample_soup,
    ):
        mock_fetch_page.return_value = sample_soup
        mock_extract_urls.return_value = {"/movie1", "/movie2"}
        mock_parse_item.side_effect = [
            CSFDObject(
                "movie",
                f"{csfd_scraper.base_url}/movie1",
                "Movie 1",
                2020,
                ["Action"],
                80,
            ),
            CSFDObject(
                "tvshow",
                f"{csfd_scraper.base_url}/movie2",
                "Show 1",
                2021,
                ["Drama"],
                90,
            ),
        ]

        result = csfd_scraper.scrape()
        assert isinstance(result, set)
        assert len(result) == 2
        assert all(isinstance(item, CSFDObject) for item in result)

    @patch("src.web_scraper.WebScraper._fetch_page")
    def test_scrape_main_page_failure(self, mock_fetch_page, csfd_scraper):
        mock_fetch_page.return_value = None
        result = csfd_scraper.scrape()
        assert result == set()
