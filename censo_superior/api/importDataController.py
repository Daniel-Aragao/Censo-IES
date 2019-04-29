from importer import Importer
from db.database import Database
from config import Config
from sheet import Sheet


class ImportDataController:
    def __init__(self, db, config, path):
        self.db = db
        self.main_config = config
        self.path_to_file = path
    
    def import_data(self):
        print("Import csv:")
        print(Importer.import_csv(self.path_to_file, self.main_config))