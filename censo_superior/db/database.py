from db.connector import Connector
from db.structure_dao import StructureDAO


class Database:
    struct_suffix = StructureDAO.struct_suffix

    def __init__(self, access_config, database_config):
        self.access_config = access_config
        self.database_config = database_config

        self.connector = Connector(access_config)
        self.connector.create_db(check_if_exists=True)

        # self.__create_general_struct_table()

        self.__create_structs_tables()

        self.structure_dao = StructureDAO(self.connector, access_config, database_config)

    # def __create_general_struct_table(self):
    # (add this property in config.json in censo_databases) "struct_table_name": "structure"
    #     exists, tables_names = self.connector.exist_tables(
    #         [self.database_config["struct_table_name"]])

    #     if not exists:
    #         connection = self.connector.make_connection()

    #         connection.execute("CREATE TABLE " + tables_names[0] + "( "
    #                            "id INT AUTO_INCREMENT PRIMARY KEY,"
    #                            "data_table_name VARCHAR(255), "
    #                            "data_struct_table_name VARCHAR(255) NOT NULL,"
    #                            "struct_insertion_date DATE NOT NULL"
    #                            ")")

    #         self.connector.close_connection()

    def __create_structs_tables(self):
        struct_tables = [table + StructureDAO.struct_suffix for table in self.database_config["tables"]]
        data_tables = [table + StructureDAO.data_suffix for table in self.database_config["tables"]]

        struct_exists, struct_tables_names = self.connector.exist_tables(struct_tables)
        data_exists, data_tables_names = self.connector.exist_tables(data_tables)

        if not struct_exists:
            connection = self.connector.make_connection()

            for table_name in struct_tables_names:
                connection.execute("CREATE TABLE " + table_name + " ("
                    "id INT AUTO_INCREMENT PRIMARY KEY,"
                    "field_name VARCHAR(100) UNIQUE NOT NULL,"
                    "synonymous TEXT NOT NULL,"
                    "field_type VARCHAR(30),"
                    "insertion_date DATE NOT NULL,"
                    "ignore_field_import TINYINT(1) NOT NULL DEFAULT 0,"
                    "ignore_field_creation TINYINT(1) NOT NULL DEFAULT 0,"
                    "last_field_update DATE NOT NULL)")

            self.connector.close_connection()
                
        
        if not data_exists:
            connection = self.connector.make_connection()

            for table_name in data_tables_names:
                connection.execute("CREATE TABLE " + table_name + " ("
                                    "id INT AUTO_INCREMENT PRIMARY KEY"
                                    ")")

            self.connector.close_connection()
