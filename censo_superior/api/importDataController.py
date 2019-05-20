from importer import Importer
from db.database import Database
from config import Config
from sheet import Sheet
import re


class ImportDataController:
    def __init__(self, db, config, path, table_name):
        self.db = db
        self.main_config = config
        self.path_to_file = path
        self.table_name = table_name
        
    
    def __build_header_map(self):
        csv_headers = Importer.import_csv_header(self.path_to_file, self.main_config)
        header_map = {}
        
        for csv_header in csv_headers:
            selected_entry = None
            db_entries, db_entries_map = self.db.structure_dao.get_by_synonym(self.table_name, csv_header)
            
            if not len(db_entries):
                raise Exception("Nenhum sinônimo encontrado para o campo informado ("+csv_header+"), tente importar o dicionário de dados equivalente ao ano do dado.")
                
            if len(db_entries) > 1:
                for db_entry in db_entries:
                    synonymous = db_entry[db_entries_map["synonymous"]].split(",")
                
                    if csv_header in synonymous:
                        if not selected_entry:
                            selected_entry = db_entry
                        else:
                            raise Exception("O campo " + csv_header + " é sinônimo de mais de um campo")
                            
            else:
                selected_entry = db_entries[0]
            
            header_map[csv_header] = {
                "field_name": selected_entry[db_entries_map["field_name"]].upper(),
                "field_type": selected_entry[db_entries_map["field_type"]].upper(),
                "ignore_field_import": bool(selected_entry[db_entries_map["ignore_field_import"]]),
                "ignore_field_creation": bool(selected_entry[db_entries_map["ignore_field_creation"]])
            }
            
        return header_map
        
        
    def import_data(self):
        header_map = self.__build_header_map()
        
        header_map_keys = [key for key in header_map if not header_map[key]["ignore_field_import"] and not header_map[key]["ignore_field_creation"]]
        
        header_map_columns = [header_map[i]["field_name"] for i in header_map_keys]
        
        ddao = self.db.data_dao
        
        connection = ddao.connector.make_connection()
        
        def bulk_function(lines):
            fields = []
            
            for line in lines:
                cells = []
                
                for header_map_key in header_map_keys:
                    cell_value = line[header_map_key]
                    
                    if header_map[header_map_key]["field_type"].find("NUM") > -1:
                        if cell_value:
                            if not cell_value.isnumeric():
                                cell_value = re.sub(r"[^.0-9]", "", cell_value)

                            if not cell_value:
                                cell_value = 0
                            else:
                                cell_value = float(cell_value)

                        else:
                            cell_value = 0

                    elif header_map[header_map_key]["field_type"].find("CHAR") > -1:
                        if cell_value:
                            cell_value = cell_value
                        else:
                            cell_value = ""
                    
                    else:
                        raise Exception("Unsupported type: " + str(header_map[header_map_key]["field_type"]))
                        
                    cells.append(cell_value)
                
                fields.append(cells)
            #print("connection:",connection)
            ddao.add_fields(fields, self.table_name, header_map_columns, use_connection=connection)
        
        Importer.import_csv(self.path_to_file, self.main_config, bulk_function)
        
        ddao.connector.commit()
        ddao.connector.close_connection()
        