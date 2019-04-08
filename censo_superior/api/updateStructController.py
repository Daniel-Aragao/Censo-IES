


class UpdateStructController:
    def __init__(self, db, config=main_config):
        self.db = db
        self.main_config = main_config
        self.imported_dict = None
    
    def import_dict(self, path):
        self.imported_dict = Importer.import_data_dictionary(path, config=main_config)
        
        # return [tabelas]

    def parse(self, table):
        # return [campos novos]
        pass
    
    def save_table(self, table, field_dict):
        # return [campos novos] (somente os que deram erro)
        pass