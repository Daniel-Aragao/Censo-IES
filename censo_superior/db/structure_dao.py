from structure import Field
from db.connector import Connector
import time


class StructureDAO:
    def __init__(self, connector: Connector, access_config, database_config):
        self.connector = connector
        self.access_config = access_config
        self.database_config = database_config

    def get_fields(self, structure_name):
        # fields: [Field] = []

        connection = self.connector.make_connection()

        connection.execute("SELECT * FROM " + structure_name)
        fetched_data = connection.fetchall()

        self.connector.close_connection()

        return fetched_data

    def add_fields(self, structure_name, field_dict):
        connection = self.connector.make_connection()
        sql = "INSERT INTO " + structure_name + \
            "(field_name, synonymous, field_type, insertion_date, ignore_field_import, last_field_update) VALUES (%s, %s, %s, %s, %s, %s)"

        time_now = time.strftime('%Y-%m-%d %H:%M:%S')

        data = map(lambda x: (x["name"], x["name"], x["type"],
                              time_now, not x["import"], time_now), field_dict)

        connection.executemany(sql, data)

        connection.execute("alte")alter table para inserir os campos adicionados

        self.connector.commit()

        self.connector.close_connection()
