from .connector import Connector


class Database:
    def __init__(self, access_config, database_config):
        self.access_config = access_config
        self.database_config = database_config

        self.connector = Connector(access_config)
        self.connector.create_db(check_if_exists=True)

        self.__create_general_struct_table()
        self.__create_structs_tables()

    def __create_general_struct_table(self):
        exists, tables_names = self.connector.exist_tables(
            [self.database_config["struct_table_name"]])

        if not exists:
            connection = self.connector.make_connection()

            connection.execute("CREATE TABLE " + tables_names[0] + "( "
                               "id INT AUTO_INCREMENT PRIMARY KEY,"
                               "data_table_name VARCHAR(255), "
                               "data_struct_table_name VARCHAR(255) NOT NULL,"
                               "struct_insertion_date DATE NOT NULL"
                               ")")

            self.connector.close_connection()

    def __create_structs_tables(self):
        exists, tables_names = self.connector.exist_tables(self.database_config["tables"])

        if not exists:
            for table_name in tables_names:
                pass
