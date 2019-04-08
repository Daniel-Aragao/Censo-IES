from config import Config
from importer import Importer
from db.database import Database
from api.updateStructController import UpdateStructController

main_config = Config('config.json').parse()
path = r"misc/Dicionário_de_Dados.xlsx"

db = Database(main_config["database_access"], main_config["censo_databases"])

updateController = UpdateStructController(db, config=main_config)

tables = updateController.import_dict(path)
table_curso = tables[1]
updateController.parse(table_curso)
# print()

##### import dictionary
# dict_sheets = Importer.import_data_dictionary(path, config=main_config)