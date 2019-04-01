from importer import Importer
from config import Config

path = r"/media/Aster/DIPLAN/Estrutura de pasta/Dicionário_de_Dados.xlsx"

Importer.config = Config('config.json')
Importer.import_data_dictionary(path)