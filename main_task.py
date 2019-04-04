from config import Config
from importer import Importer
from db.connector import Connector

main_config = Config('config.json')

path = r"misc/Dicionário_de_Dados.xlsx"
dict_sheets = Importer.import_data_dictionary(path, config=main_config)

Connector(main_config["database_access"])

Compare