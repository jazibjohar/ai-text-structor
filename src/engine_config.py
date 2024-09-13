import json


def load_json(file_path):
    with open(file_path) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d
