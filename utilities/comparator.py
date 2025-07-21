import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_to_json(data, filename = "old_announcements.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_from_json(filename = "old_announcements.json"):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
    
def compare_to_json(data, filename = "old_announcements.json"):
    try:
        old_data = load_from_json(filename)
    except FileNotFoundError:
        old_data = []
    

    if len(data) < len(old_data):
        logging.critical("New data is shorter than old data, skipping comparison.")
        return []
    
    new_data = [item for item in data if item not in old_data]

    if new_data:
        logging.info(f"Found {len(new_data)} new updates.")
        save_to_json(data, filename)
        return new_data
    else:
        logging.info("No new updates found.")
        return []