import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_info(url):
    try:
        logging.info(f"Fetching data from {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        logging.info("Data fetched successfully")
        return response.text  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        logging.critical(f"An error occurred: {e}")
        return None