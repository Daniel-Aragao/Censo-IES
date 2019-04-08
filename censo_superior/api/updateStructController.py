from importer import Importer


class UpdateStructController:
    def __init__(self, db, config):
        self.db = db
        self.main_config = config
        self.imported_dict = None
    
    def import_dict(self, path):
        self.imported_dict = Importer.import_data_dictionary(path, config=self.main_config)
        # return [(sheet, self.imported_dict[sheet]["name"]) for sheet in self.imported_dict]
        return [sheet for sheet in self.imported_dict]

    def parse(self, table):
        sheet = self.imported_dict[table]
        print(sheet.data)
        # old_fields = self.db.structure_dao.get_fields(table)
        # return [campos novos]
        pass
    
    def save_table(self, table, field_dict):
        # return [campos novos] (somente os que deram erro)
        pass