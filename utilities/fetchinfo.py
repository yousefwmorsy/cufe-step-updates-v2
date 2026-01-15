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

def fetch_info(url):
    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url, headers=HEADERS, timeout=15)
        logging.info("Data fetched successfully")
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        logging.critical(f"An error occurred: {e}")
        return None