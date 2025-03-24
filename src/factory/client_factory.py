
import importlib

class ClientFactory:
    @staticmethod
    def create_client(class_path, settings, common_map, additional_map, constant_map, base_url, logger):
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        client_class = getattr(module, class_name)
        return client_class(settings, common_map, additional_map, constant_map, base_url, logger)
