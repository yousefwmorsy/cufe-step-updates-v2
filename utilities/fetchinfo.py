import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "ar,en-US;q=0.9,en;q=0.8",
}

def fetch_info_html(url):
    logging.info(f"Fetching data from {url}")
    response = requests.get(url)
    logging.info("Data fetched successfully")
    logging.critical(f"Response preview: {response.text}")
    return response.text

def fetch_info(url):
    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url, headers=HEADERS, timeout=30)
        logging.info("Data fetched successfully")
        logging.info(f"Status: {response.status_code}")
        logging.info(f"Content-Type: {response.headers.get('Content-Type')}")

        response.raise_for_status()

        if not response.text.strip():
            raise ValueError("Empty response body")

        if "application/json" not in response.headers.get("Content-Type", ""):
            raise ValueError("Response is not JSON")

        return response.json()

    except Exception as e:
        logging.critical(f"Fetch failed for {url}: {e}")
        logging.critical(f"Response preview: {response.text[:300] if 'r' in locals() else 'No response'}")
        return None

    except requests.exceptions.RequestException as e:
        logging.critical(f"An error occurred: {e}")
        return None
