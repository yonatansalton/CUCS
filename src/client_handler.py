
from factory.client_factory import ClientFactory
import os
import shutil
import json

class ClientHandler:
    def __init__(self, settings, logger):
        self.common_map = settings["common_map"]
        self.apis = settings["apis"]
        self.clients = []
        self.buffer_size = settings["buffer_size"]
        self.output_file = settings["output_file"]
        self.logger = logger

        for api_conf in self.apis:
            if api_conf.get("enabled"):
                self.clients.append(
                    ClientFactory.create_client(
                        settings = api_conf,
                        class_path=api_conf["class_path"],
                        common_map=self.common_map,
                        additional_map=api_conf.get("additional_map", []),
                        constant_map=api_conf.get("constant_map", []),
                        base_url=api_conf.get("base_url"),
                        logger = self.logger
                    )
                )

    def fetch_raw_data_to_disk(self):
        buffer = []

        for client in self.clients:
            self.logger.info(f"Fetching raw data from {client.__class__.__name__}")
            raw_path = client.settings["raw_path"]
            if os.path.exists(os.path.dirname(raw_path)):
                shutil.rmtree(os.path.dirname(raw_path))
            os.makedirs(os.path.dirname(raw_path), exist_ok=True)
            for data in client.fetch_data():
                buffer.append(json.dumps(data) + "\n")
                if len(buffer) >= self.buffer_size:
                    with open(raw_path, 'a', encoding='utf-8') as f:
                        f.writelines(buffer)
                    buffer.clear()

            # Write remaining data after loop
            if buffer:
                with open(raw_path, 'a', encoding='utf-8') as f:
                    f.writelines(buffer)
            buffer.clear()
            self.logger.info(f"Finished to fetch raw data from {client.__class__.__name__}")

    def normalize_data_from_disk(self):
        buffer = []

        for client in self.clients:
            self.logger.info(f"Normalizing data for {client.__class__.__name__}")
            raw_path = client.settings["raw_path"]
            norm_path = client.settings["norm_path"]

            if not os.path.exists(raw_path):
                continue

            # Clean or create the norm path directory
            if os.path.exists(norm_path):
                os.remove(norm_path)

            with open(raw_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    normalized = client.normalize(data)
                    buffer.append(json.dumps(normalized) + "\n")

                    if len(buffer) >= self.buffer_size:
                        with open(norm_path, 'a', encoding='utf-8') as nf:
                            nf.writelines(buffer)
                        buffer.clear()

            # Write any remaining normalized data
            if buffer:
                with open(norm_path, 'a', encoding='utf-8') as nf:
                    nf.writelines(buffer)
                buffer.clear()
            self.logger.info(f"Finished Normalizing data for {client.__class__.__name__}")
        

    def aggregate_and_sort_normalized(self):
        self.logger.info(f"Started aggregating and sorting data")
        aggregated = []

        # Read all normalized files from clients
        for client in self.clients:
            norm_path = client.settings["norm_path"]
            if not os.path.exists(norm_path):
                continue

            with open(norm_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    aggregated.append(data)

        # Sort the aggregated data by 'name'
        aggregated.sort(key=lambda x: x.get('name', '').lower())

        # Save the sorted result to the output file as a JSON array
        with open(self.output_file, 'w', encoding='utf-8') as out_file:
            json.dump(aggregated, out_file, ensure_ascii=False, indent=2)

        # Print to console
        for item in aggregated:
            print(item)

