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
    
    def create_db(self):
        exist = self.exist_db()

        if not exist:
            self.make_connection()

            self.execute("CREATE DATABASE " + self.name)

            self.close_connection()
        
