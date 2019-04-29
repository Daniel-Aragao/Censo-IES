from structure import Field
from db.connector import Connector


class DataDAO:
    data_suffix = "_data"
    struct_suffix = "_struct"

    def __init__(self, connector: Connector, database_config):
        self.connector = connector
        self.database_config = database_config
    
    def add_fields(fields, commit=False):
        pass