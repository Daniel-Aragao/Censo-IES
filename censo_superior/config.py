import json as JSON
from os import path as PATH


class Config:
    def __init__(self, path):
        self.__config_structure = None
        self.__path = None

        self.reload_path(path)
    
    def get_path(self):
        return self.__path
    
    def parse(self):
        if not self.__config_structure:
            with open(self.__path, 'r', encoding="utf8") as file_obj:
                string = file_obj.read().replace('\n', '')
                
                self.__config_structure = JSON.loads(string)
        
        return self.__config_structure

    def reload_path(self, path):
        if not PATH.exists(path):
            raise Exception("Config file not found on path: " + str(path))

        self.__config_structure = None

        self.__path = path