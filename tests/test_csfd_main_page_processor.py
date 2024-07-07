import pytest
from bs4 import BeautifulSoup

from src.csfd_main_page_processor import CSFDMainPageProcessor


class TestCSFDPageProcessor:
    @pytest.fixture
    def page_processor(self):
        return CSFDMainPageProcessor(["Test Section"])

    def test_extract_top_items_urls(self, page_processor, sample_soup):
        result = page_processor.extract_top_items_urls(sample_soup)
        assert result == set()  # No matching sections in our sample HTML

    def test_extract_top_items_urls_no_match(self, page_processor):
        soup = BeautifulSoup("<html><h2>No Match</h2></html>", "html.parser")
        result = page_processor.extract_top_items_urls(soup)
        assert result == set()

    @pytest.mark.parametrize(
        "input_url, expected",
        [
            ("/show/episode/123/", "/show/episode/"),
            ("/movie/123/", "/movie/123/"),
        ],
    )
    def test_trim_episode_url_endpoint(self, input_url, expected):
        assert CSFDMainPageProcessor.trim_episode_url_endpoint(input_url) == expected
