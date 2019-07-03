from structure import Field
from db.connector import Connector


class DataDAO:
    data_suffix = "_data"
    struct_suffix = "_struct"

    def __init__(self, connector: Connector, database_config):
        self.connector = connector
        self.database_config = database_config
    
    def add_fields(self, fields, table_name, columns, use_connection=None):
        if not use_connection:
            connection = self.connector.make_connection()
        else:
            connection = use_connection
        
        sql_insert = "INSERT INTO " + table_name + \
            "(" + ",".join([i for i in columns]) + ", import_year) VALUES (" + ",".join(["%s" for i in columns]) + ", %s)"
        
        connection.executemany(sql_insert, fields)

        if not use_connection:
            self.connector.commit()
            self.connector.close_connection()
            