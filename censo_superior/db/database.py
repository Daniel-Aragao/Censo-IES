from db.connector import Connector
from db.structure_dao import StructureDAO
from db.data_dao import DataDAO


class Database:
    struct_suffix = StructureDAO.struct_suffix

    def __init__(self, access_config, database_config):
        self.access_config = access_config
        self.database_config = database_config

        self.connector = Connector(access_config)
        self.connector.create_db(check_if_exists=True)
        
        self.__create_structs_tables()

        self.structure_dao = StructureDAO(self.connector, database_config)
        self.data_dao = DataDAO(self.connector, database_config)
        
    def get_existent_tables(self, suffix=""):
        """
        Access the database and get the tables available
        return (not_created_tables_names: [str], created_tables_names: [str])
        """
        struct_tables = [table.lower() + suffix for table in self.database_config["tables"]]
        return self.connector.exist_tables(struct_tables)
        
    
    def get_existent_data_table(self):
        """
        Access the database and get the tables available
        return (not_created_tables_names: [str], created_tables_names: [str])
        """
        return self.get_existent_tables(StructureDAO.data_suffix)

    def __create_structs_tables(self):
        not_created_struct_tables_names, created_struct_tables_names = self.get_existent_tables(StructureDAO.struct_suffix)
        not_created_data_tables_names, created_data_tables_names = self.get_existent_data_table()

        if len(not_created_struct_tables_names):
            connection = self.connector.make_connection()

            for table_name in not_created_struct_tables_names:
                connection.execute("CREATE TABLE " + table_name.lower() + " ("
                    "id INT AUTO_INCREMENT PRIMARY KEY,"
                    "field_name VARCHAR(100) UNIQUE NOT NULL,"
                    "field_description TEXT,"
                    "synonymous TEXT NOT NULL,"
                    "field_type VARCHAR(30),"
                    "insertion_date DATE NOT NULL,"
                    "ignore_field_import TINYINT(1) NOT NULL DEFAULT 0,"
                    "ignore_field_creation TINYINT(1) NOT NULL DEFAULT 0,"
                    "last_field_update DATE NOT NULL)")

                print("Table created: " + str(table_name))
            self.connector.close_connection()
                
        
        if len(not_created_data_tables_names):
            connection = self.connector.make_connection()

            for table_name in not_created_data_tables_names:
                connection.execute("CREATE TABLE " + table_name.lower() + " ("
                                    "id INT AUTO_INCREMENT PRIMARY KEY"
                                    ")")
                                    
                print("Table created: " + str(table_name))

            self.connector.close_connection()
