
from abc import ABC, abstractmethod

class APIClient(ABC):
    def __init__(self, settings, common_map, additional_map, constants_map, base_url, logger):
        self.settings = settings
        self.limit = settings["limit_results"]
        self.common_map = common_map
        self.additional_map = additional_map
        self.base_url = base_url
        self.constant_map = constants_map
        self.merged_map = self.common_map | self.additional_map
        self.logger = logger

    @abstractmethod
    def fetch_data(self):
        pass

    def normalize(self, raw_data):
        normalized = {}
        for key,value in self.merged_map.items():
            if value not in raw_data:
                self.logger.warning(f"Missing '{key}' in API response from {self.__class__.__name__}")
            normalized[key] = raw_data.get(value, None)
        for key,value in self.constant_map.items():
            normalized[key] = value

        return normalized
