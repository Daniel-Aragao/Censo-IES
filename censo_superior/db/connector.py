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
                user=self.user,
                passwd=config["password"]
            )
        
        self.connection = None
    
    def make_connection(self, use_db=True):
        # TODO: Observar implicações no parametro buffered=True abaixo:        
        self.connection = self.__db_connector.cursor(buffered=True)

        if use_db:
            self.connection.execute("use " + self.name + ";")

        return self.connection

    def close_connection(self):
        # self.connection.fetchall()
        self.connection.close()
        
    def exist_db(self):
        self.make_connection(use_db=False)
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
            self.make_connection(use_db=False)

            self.connection.execute("CREATE DATABASE " + self.name)

            self.close_connection()
    
    def exist_tables(self, tables_names):
        self.make_connection()

        self.connection.execute("use " + self.name + ";")
        self.connection.execute("SHOW TABLES")

        not_created = []
        
        db_tables = [db[0] for db in self.connection]

        for table_name in tables_names:
            if not (table_name in db_tables):
                not_created.append(table_name)
        
        self.close_connection()

        return (not bool(len(not_created))), not_created
        
