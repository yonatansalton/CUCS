
import requests
from .base_client import APIClient

import requests

class RickAndMortyClient(APIClient):
    def fetch_data(self):
        next_url = self.base_url
        count = 0

        while next_url:
            try:
                response = requests.get(next_url, timeout=10)
                response.raise_for_status()
                data = response.json()
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Failed to fetch data from {next_url}: {e}")
                break  
            except ValueError as e:
                self.logger.error(f"Invalid JSON received from {next_url}: {e}")
                break

            for character in data.get('results', []):
                if self.limit is not None and count >= self.limit:
                    return
                yield character
                count += 1

            next_url = data.get('info', {}).get('next')
