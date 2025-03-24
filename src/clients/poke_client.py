from .base_client import APIClient
import requests

class PokeAPIClient(APIClient):
    def fetch_data(self):
        next_url = self.base_url
        count = 0

        while next_url and count < self.limit:
            response = requests.get(next_url)
            response.raise_for_status()
            data = response.json()

            for pokemon in data.get('results', []):
                if count >= self.limit:
                    break
                try:
                    detail_response = requests.get(pokemon['url'])
                    detail_response.raise_for_status()
                    pokemon_details = detail_response.json()
                    yield pokemon_details  
                    count += 1
                except requests.RequestException as e:
                    self.logger.warning(f"Failed fetching details for {pokemon['name']}: {e}")

            next_url = data.get('next') 

    def normalize(self, raw_data):
        normalized = super().normalize(raw_data)
        types = sorted(raw_data['types'], key=lambda x: x['slot'])
        type_names = [t['type']['name'].capitalize() for t in types]
        normalized["species"] = "/".join(type_names)
        
        return normalized