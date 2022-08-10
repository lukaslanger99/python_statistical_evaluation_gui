import json
from typing import Union, Dict, List


class FileHandler:
    def read_json_file_to_dict_list(self, path: str) -> List[Dict[str, Union[str, int]]]:
        try:
            with open(path, "r") as read_file:
                data = json.load(read_file)
            return data
        except:
            return []

    def write_dict_list_to_json_file(self, path: str, dict: List[Dict[str, Union[str, int]]]):
        with open(path, 'w') as write_file:
            json.dump(dict, write_file)
