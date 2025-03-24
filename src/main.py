
import json
from client_handler import ClientHandler
from utils.logger import get_logger

def load_settings():
    with open("settings.json") as f:
        return json.load(f)

def main():
    settings = load_settings()
    logger = get_logger(settings)
    handler = ClientHandler(settings, logger)
    handler.fetch_raw_data_to_disk()
    handler.normalize_data_from_disk()
    handler.aggregate_and_sort_normalized()

if __name__ == "__main__":
    main()
