

class UpdateStructController:
    def __init__(self, db):
        self.db = db
    
    def import_dict(self, path):
        # return [tabelas]
        pass

    def parse(self, table):
        # return [campos novos]
        pass
    
    def save_table(self, table, field_dict):
        # return [campos novos] (somente os que deram erro)
        pass