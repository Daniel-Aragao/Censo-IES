import time

from structure import Field
from db.connector import Connector


class StructureDAO:
    data_suffix = "_data"
    struct_suffix = "_struct"

    def __init__(self, connector: Connector, access_config, database_config):
        self.connector = connector
        self.access_config = access_config
        self.database_config = database_config

    def get_fields(self, structure_name):
        # fields: [Field] = []

        connection = self.connector.make_connection()

        connection.execute(
            "SELECT  id, field_name, synonymous, field_type, insertion_date, ignore_field_import FROM " + structure_name)
        fetched_data = connection.fetchall()

        self.connector.close_connection()

        return fetched_data, {"id": 0, "field_name": 1, "synonymous": 2, "field_type": 3, "insertion_date": 4, "ignore_field_import": 5}

    def get_type(self, type_db):
        type_db = type_db.lower()

        types = self.database_config["types"]

        if not type_db in types:
            raise Exception(
                "Unsuported type, add a new type map in config.json: " + type_db)

        return types[type_db.lower()]

    def add_fields(self, structure_name, field_dict):
        connection = self.connector.make_connection()
        sql_insert = "INSERT INTO " + structure_name + StructureDAO.struct_suffix + \
            "(field_name, field_description, synonymous, field_type, insertion_date, ignore_field_import, last_field_update) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        time_now = time.strftime('%Y-%m-%d %H:%M:%S')

        data_insert = map(lambda x: (x["name"], x["description"], x["name"], x["type"],
                                     time_now, not x["import"], time_now), field_dict)

        connection.executemany(sql_insert, data_insert)

        sql_alter = "ALTER TABLE " + structure_name + \
            StructureDAO.data_suffix  # + "ADD COLUMN (%s %s)"
        # data_alter = map(lambda x: (x["name"], self.get_type(x["type"])), field_dict)

        # connection.executemany(sql_insert, data_alter)

        for index, field in enumerate(field_dict):
            sql_alter += " ADD COLUMN " + \
                field["name"] + " " + self.get_type(field["type"])

            if index < len(field_dict) - 1:
                sql_alter += ","
        connection.execute(sql_alter)

        self.connector.commit()

        self.connector.close_connection()

    def update_synonym(self, table, new_synonyms):
        connection = self.connector.make_connection()

        sql_update = "UPDATE " + table + StructureDAO.struct_suffix + " SET synonymous = synonymous + %s WHERE id = %s"

        for new_synonym in new_synonyms:
            connection.execute(sql_update, new_synonym)

        self.connector.commit()

        self.connector.close_connection()
