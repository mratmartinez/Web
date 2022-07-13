from types import ModuleType, FunctionType
import os

import json
import markdown

import yaml

class Worker(object):
    def __init__(
            self,
            json_parser: ModuleType = json,
            markdown_parser: ModuleType = markdown,
            yaml_parser: ModuleType = yaml
            ):
        self._json_decoder = json_parser.JSONDecoder()
        self._markdown_parser = markdown_parser.Markdown()
        self._yaml_parser = yaml_parser
        # Properties
        self._root_directory: str = '.'
        return

    @property
    def root_directory(self):
        return self._root_directory

    @root_directory.setter
    def root_directory(self, directory: str):
        if not (os.path.isdir(directory)):
            raise Exception(f'{directory} is not a valid directory.')
        self._root_directory = directory
        return

    @classmethod
    def get_worker_for_directory(cls, directory: str):
        worker = cls()
        worker.root_directory = directory
        return worker

    @staticmethod
    def get_filename_filter(extension: str) -> FunctionType:
        if not (extension.startswith('.') and len(extension)>1):
            raise Exception(f'{extension} is not a valid extension suffix.')
        lowercase_extension: str = extension.lower()
        def filename_filter(filename: str) -> bool:
            lowercase_filename: str = filename.lower()
            if (lowercase_filename.endswith(lowercase_extension) and not lowercase_filename.startswith('.')):
                return True
            return False
        return filename_filter

    def filter_root_for_markdown(self) -> filter:
        files: list = os.listdir(self.root_directory)
        filename_filter: FunctionType = self.get_filename_filter('.md')
        filtered_files: filter = filter(filename_filter, files)
        return filtered_files

    def read_file(self, filename: str):
        try:
            filepath: str = os.path.join(self.root_directory, filename)
            if not (os.path.exists(filepath)):
                raise Exception(f'{filename} doesn\'t exist.')
        except Exception as e:
            raise e
        file = open(filepath, 'r')
        return file

    def get_file_header(self, file):
        if not (file.read(5) == '%YAML'):
            raise Exception('Header doesn\'t include YAML version.')
        try:
            version: float = float(file.readline().strip())
            if (version < 1.2):
                raise Exception('This YAML version is not supported.')
            file.seek(0)
            yaml_buffer: str = ''
            for line in file:
                yaml_buffer += line
                if (line.strip() == '...'):
                    break
            if ('\n...\n' not in yaml_buffer):
                raise Exception('YAML end mark not in header.')
            markdown: str = file.read().strip()
            file.close()
            return (yaml_buffer, markdown)
        except Exception as e:
            raise e

    def get_posts(self):
        file_list: list = self.filter_root_for_markdown()
        post_list: list = []
        for filename in file_list:
            try:
                file = self.read_file(filename)
                header, markdown = self.get_file_header(file)
                post_list.append({
                    'header': header,
                    'markdown': markdown
                })
            except Exception as e:
                raise e
        return post_list

    def read_header(self, header: str):
        parsed_yaml = self._yaml_parser.load(header, Loader=self._yaml_parser.Loader)
        return parsed_yaml
