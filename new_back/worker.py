from types import ModuleType
import os

import json
import markdown

class Worker(object):
    def __init__(
            self,
            json_parser: ModuleType = json,
            markdown_parser: ModuleType = markdown
            ):
        self._json_decoder = json_parser.JSONDecoder()
        self._markdown_parser = markdown_parser.Markdown()
        # Properties
        self._root_directory: str = '.'
        return

    @property
    def root_directory(self):
        return self._root_directory

    @root_directory.setter
    def root_directory(self, directory: str):
        if not (os.path.isdir(directory)):
                raise Exception(f'{directory} is not a valid directory')
        self._root_directory = directory
        return

    @classmethod
    def get_worker_for_directory(cls, directory: str):
        worker = cls()
        worker.root_directory = directory
        return worker

