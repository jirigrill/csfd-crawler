# CSFD Scraper

## Overview

CSFD Scraper is a Python-based web scraping tool designed to extract movie and TV show information from the Česko-Slovenská filmová databáze (CSFD) website. This project allows users to programmatically retrieve details such as titles, ratings, genres, and release years for films and television series listed on CSFD.

## Features

- Scrapes movie and TV show data from CSFD's most visited sections
- Extracts key information including:
  - Title (with preference for US titles when available)
  - Type (movie or TV show)
  - Year of release
  - Genres
  - User rating
- Handles pagination to retrieve multiple pages of results
- Robust error handling and logging
- Configurable to focus on specific sections of the CSFD website

## Requirements

- Python 3.12.4+
- BeautifulSoup4
- Requests

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/csfd-scraper.git
   cd csfd-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the CSFD Scraper, run the main script:

```python
from src.csfd_scraper import CSFDScraper

BASE_URL = "https://www.csfd.cz"
HEADERS = {"User-Agent": "Your User Agent String"}
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
```

## Configuration

No configuration is available at the moment.

## Testing

To run the unit tests:

```
pytest tests/
```

## Contributing

Contributions to the CSFD Scraper project are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This scraper is for educational purposes only. Please be mindful of CSFD's terms of service and use this tool responsibly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.