from connector import Connector


class Database:
    def __init__(self, access_config, database_config):
        self.access_config = access_config
        self.database_config = database_config

        self.connector = Connector(access_config)
        self.connector.create_db(check_if_exists=True)

        self.create_struct_table()

    def create_struct_table(self):
        exists = self.connector.exist_table(
            database_config["struct_table_name"])

        if not exists:
            # connection = self.connector.make_connection()

            # connection.execute("CREATE TABLE "+ database_config["struct_table_name"]+ "( "
            #     "id INT AUTO_INCREMENT PRIMARY KEY," 
            #     "name VARCHAR(255), "
            #     "address VARCHAR(255)
            #     ")")

            # self.connector.close_connection()
            pass
