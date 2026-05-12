import os
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def scrape_medium_article(url):
    logger.info("Starting scrape for URL: %s", url)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    logger.debug("Request headers prepared: %s", headers)

    try:
        logger.info("Sending GET request...")
        response = requests.get(url, headers=headers, timeout=15)
        logger.info("Response received. Status code: %d", response.status_code)
        logger.info("Response size: %d bytes", len(response.content))
    except requests.RequestException as e:
        logger.error("Request failed: %s", e)
        return None

    if response.status_code != 200:
        logger.warning("Non-200 status code. Aborting.")
        return None

    logger.info("Parsing HTML with BeautifulSoup...")
    soup = BeautifulSoup(response.text, "html.parser")

    logger.info("Extracting <p> tags...")
    paragraphs = soup.find_all("p")
    logger.info("Found %d paragraphs", len(paragraphs))

    if not paragraphs:
        logger.warning("No paragraphs found. Page may use JS rendering or be paywalled.")

    logger.info("Joining paragraph text...")
    article_text = "\n\n".join(p.get_text() for p in paragraphs)
    logger.info("Total extracted characters: %d", len(article_text))

    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "scraped_article.txt")
    logger.info("Saving to file: %s", file_path)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(article_text)
        logger.info("File written successfully.")
    except OSError as e:
        logger.error("Failed to write file: %s", e)
        return None

    logger.info("Article successfully scraped!")
    return file_path


if __name__ == "__main__":
    url = "https://medium.com/@cordobatoro.mateo/the-internet-gap-growth-challenges-and-the-future-9a73a9d8de21"
    result = scrape_medium_article(url)
    logger.info("Final result path: %s", result)