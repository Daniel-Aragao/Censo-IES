from structure import Field
from db.connector import Connector


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


