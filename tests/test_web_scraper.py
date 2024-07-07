import pytest
from unittest.mock import patch
import requests
from bs4 import BeautifulSoup

from src.web_scraper import WebScraper


class TestWebScraper:
    @pytest.fixture
    def web_scraper(self, base_url, headers):
        return WebScraper(base_url, headers)

    def test_fetch_page_success(self, web_scraper, mock_response, sample_html):
        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_response(sample_html, 200)
            result = web_scraper._fetch_page(web_scraper.base_url)
            assert isinstance(result, BeautifulSoup)
            expected_soup = BeautifulSoup(sample_html, "html.parser")
            assert result.prettify() == expected_soup.prettify()

    def test_fetch_page_failure(self, web_scraper, mock_response):
        with patch("requests.get") as mock_get:
            mock_get.return_value = mock_response("Error", 404)
            with pytest.raises(requests.exceptions.HTTPError):
                web_scraper._fetch_page(web_scraper.base_url)
