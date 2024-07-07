import pytest
from bs4 import BeautifulSoup
import requests


@pytest.fixture
def sample_html():
    return """
    <html>
        <div class="film-header-name">
            <h1>Test Movie</h1>
            <span class="type">TV Series</span>
        </div>
        <ul class="film-names">
            <li><img title="USA">US Title</li>
        </ul>
        <div class="genres">Action / Drama</div>
        <div class="film-rating-average">85%</div>
        <div class="origin"><span>2020</span></div>
    </html>
    """


@pytest.fixture
def sample_soup(sample_html):
    return BeautifulSoup(sample_html, "html.parser")


@pytest.fixture
def mock_response():
    class MockResponse:
        def __init__(self, text, status_code):
            self.text = text
            self.status_code = status_code

        def raise_for_status(self):
            if self.status_code >= 400:
                raise requests.exceptions.HTTPError(f"HTTP Error: {self.status_code}")

    return MockResponse


@pytest.fixture
def base_url():
    return "https://www.csfd.cz"


@pytest.fixture
def headers():
    return {"User-Agent": "CSFD Scraper Test"}
