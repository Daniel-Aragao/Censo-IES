from config import Config
from importer import Importer
from db.database import Database

main_config = Config('config.json').parse()

db = Database(main_config["database_access"], main_config["censo_databases"])

##### import dictionary
# path = r"misc/Dicionário_de_Dados.xlsx"
# dict_sheets = Importer.import_data_dictionary(path, config=main_config)