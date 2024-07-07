import pytest
from bs4 import BeautifulSoup

from src.csfd_object import CSFDObject
from src.csfd_item_parser import CSFDItemParser


class TestCSFDParser:
    @pytest.fixture
    def csfd_parser(self, sample_soup, base_url):
        return CSFDItemParser(sample_soup, f"{base_url}/movie")

    def test_parse_item(self, csfd_parser):
        result = csfd_parser.parse_item()
        assert isinstance(result, CSFDObject)
        assert result.type == "tvshow"
        assert result.name == "US Title"
        assert result.year == 2020
        assert result.genre == ["Action", "Drama"]
        assert result.rating == 85

    def test_parse_item_no_us_title(self, csfd_parser):
        csfd_parser.html_page.find("ul", {"class": "film-names"}).decompose()
        result = csfd_parser.parse_item()
        assert isinstance(result, CSFDObject)
        assert result.name == "Test Movie"

    def test_parse_item_no_data(self, csfd_parser, base_url):
        csfd_parser.html_page = BeautifulSoup("<html></html>", "html.parser")
        result = csfd_parser.parse_item()
        assert result is None
