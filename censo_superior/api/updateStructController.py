from importer import Importer
from db.database import Database
from config import Config
from sheet import Sheet


class UpdateStructController:
    def __init__(self, db: Database, config: Config):
        self.db = db
        self.main_config = config
        self.__imported_dict = None
    
    def import_dict(self, path):
        self.__imported_dict = Importer.import_data_dictionary(path, config=self.main_config)
        return list(self.__imported_dict.keys())

    def parse(self, table):
        sheet: Sheet = self.__imported_dict[table]
        old_fields = self.db.structure_dao.get_fields(table + Database.struct_suffix)
        diff_fields = []

        if old_fields and len(old_fields):
            # comparar campos e retornar as diferenças já eliminando os que possuem sinonimos
            pass
        else:
            diff_fields = [(data["name"], data["description"], data["type"]) for data in sheet.data]
        
        return diff_fields
            
        # return [campos novos]
    
    def save_table(self, table, field_dict):
        # return [campos novos] (somente os que deram erro)
        old_fields = self.db.structure_dao.get_fields(table + Database.struct_suffix)
        errors = []
        if old_fields and len(old_fields):
            # verificar se algum sinonimo passado por parametro corresponde 
            # ao nome de algum campo
            pass
        else:
            self.db.structure_dao.add_fields(table, field_dict)

        return errors
            
