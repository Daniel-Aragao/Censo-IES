import mysql.connector

class Connector:
    def __init__(self, config):
        """
        Create connection with the given database passed on config parameter
        config properties:
            name = database name
            user = user to connect
            password = password to connect (won't save it)
            host = address to the database server            
        """

        self.name = config["name"]
        self.user = config["user"]
        # self.password = config["password"]
        self.host = config["host"]

        self.__db_connector = mysql.connector.connect(
                host=self.host,
                user=self.name,
                passwd=config["password"]
            )
        
        self.connection = None
    
    def make_connection(self):        
        self.connection = self.__db_connector.cursor()
        return self.connection

    def close_connection(self):
        self.connection.close()
        
    def exist_db(self):
        self.make_connection()

        self.connection.execute("SHOW DATABASES")

        for db in self.connection:
            if db[0] == self.name:
                return True
        
        self.close_connection()

        return False
    
    def create_db(self, check_if_exists=True):
        if check_if_exists:
            exist = self.exist_db()

        if not check_if_exists or (check_if_exists and not exist):
            self.make_connection()

            self.execute("CREATE DATABASE " + self.name)

            self.close_connection()
    
    def exist_table(self, table_name):
        self.make_connection()

        self.connection.execute("SHOW TABLES")

        for db in self.connection:
            if db[0] == table_name:
                return True
        
        self.close_connection()

        return False
        
