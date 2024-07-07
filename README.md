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
- Docker support for easy deployment and execution

## Requirements

- Python 3.12+
- BeautifulSoup4
- Requests
- Docker (optional, for containerized execution)

## Installation

### Local Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/csfd-scraper.git
   cd csfd-scraper
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Docker Installation

1. Ensure you have Docker installed on your system.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/csfd-scraper.git
   cd csfd-scraper
   ```

## Usage

### Local Usage

To use the CSFD Scraper locally, run the main script:

```python
python main.py
```

### Docker Usage

To use the CSFD Scraper with Docker:

1. Build the Docker image:
   ```
   docker build -t csfd-scraper .
   ```

2. Run the Docker container:
   ```
   docker run csfd-scraper
   ```

This will execute the scraper inside a Docker container and output the results.

## Configuration

No configuration is available at the moment.

## Testing

To run the unit tests:

```
pytest tests/
```

## Docker

The project includes a Dockerfile for easy containerization. The Dockerfile:

- Uses Python 3.12 slim image as the base
- Sets up the necessary environment variables
- Installs system and Python dependencies
- Copies the application code into the container
- Creates a non-root user for enhanced security
- Specifies the command to run the scraper

To build and run the Docker image, follow the Docker Usage instructions in the Usage section above.

## Contributing

Contributions to the CSFD Scraper project are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This scraper is for educational purposes only. Please be mindful of CSFD's terms of service and use this tool responsibly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.