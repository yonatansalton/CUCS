
import requests
from .base_client import APIClient

import requests

class SWAPIClient(APIClient):
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

            for item in data.get('results', []):
                if self.limit is not None and count >= self.limit:
                    return
                yield item
                count += 1

            next_url = data.get('next') 

    def normalize(self, raw_data):
        normalized = super().normalize(raw_data)
        if "species" in raw_data and raw_data["species"]: 
            url = raw_data["species"][0]
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            species_name = data['name']
        else:
            species_name = "unknown"
            

        normalized["species"] = species_name
        
        return normalized
