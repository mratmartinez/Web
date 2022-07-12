from types import ModuleType
import json

class Worker(object):
    def __init__(self, json_parser: ModuleType = json):
        self._json_decoder = json_parser.JSONDecoder()
        print(self._json_decoder)
