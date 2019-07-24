import csv
import pandas
import math
from sheet import Sheet
from config import Config


class Importer:
    config = None
    
    @staticmethod
    def import_csv_header(path: str, config=None):
        if config:
            Importer.config = config.parse()
        
        data_file_config = Importer.config["data_csv_file"]
        lines_limit = data_file_config["lines_limit"]
        
        with open(path, encoding=data_file_config["encoding"]) as file_obj_control:
            reader = csv.DictReader(file_obj_control, delimiter=data_file_config["delimiter"])
            fields = reader.fieldnames
            
        return fields

    @staticmethod
    def import_csv(path: str, config=None, bulk=None):
        if config:
            Importer.config = config.parse()
        
        data_file_config = Importer.config["data_csv_file"]
        lines_limit = data_file_config["lines_limit"]
        bulk_limit = data_file_config["bulk_limit"]
        
        lines = []
        count = 0

        with open(path, encoding=data_file_config["encoding"]) as file_obj_control:
            reader = csv.DictReader(file_obj_control, delimiter=data_file_config["delimiter"])
            #len(reader)
            for row in reader:
                lines.append(row)
                
                count += 1
                
                if bulk and not (count % bulk_limit) and len(lines):
                    bulk(lines)
                    lines = []
                    # print("Progresso: " + str(count/file_obj_control))
                
                if lines_limit and count >= lines_limit:
                    break
        
        if bulk and len(lines):
            bulk(lines)
        else:
            return lines

    @staticmethod
    def import_workbook(path):
        return pandas.ExcelFile(path)
    
    @staticmethod
    def import_sheet_names(path):
        return Importer.import_workbook(path).book.sheet_names()

    @staticmethod
    def import_sheet_from_workbook(workbook: pandas.io.excel.ExcelFile, sheet_name, header=1, path: str=None):
        if workbook:
            return workbook.parse(sheet_name, header=header)
        else:
            return Importer.import_workbook(path).parse(sheet_name, header=header)
    
    @staticmethod
    def import_sheet_columns(sheet: pandas.core.frame.DataFrame=None, path: str=None, sheet_name: str = None, header=1):
        """
            Read sheet header from 
                a string path with a default header line as 1 and another string with sheet name
                or 
                a pandas.core.frame.DataFrame object
        """
        if sheet:
            return sheet.columns
        else:
            return Importer.import_workbook(path).parse(sheet_name, header=header).columns
    
    @staticmethod
    def get_sheet_names_from_workbook(workbook: pandas.io.excel.ExcelFile):
        return workbook.sheet_names
    
    @staticmethod
    def clean_columns(columns, dict_config):
        new_columns = list(filter(lambda x: str(x).lower().find("unnamed") < 0, list(columns)))
        new_columns = list(map(lambda x: str(x).replace("\n",'').upper(), new_columns))

        columns_to_return = []

        for new_column in new_columns:
            for column_key in dict_config:
                column_config = dict_config[column_key]

                if new_column.upper() == column_config["name"].upper():
                    columns_to_return.append({"sheet_column": new_column, "column_key": column_key, "mandatory": column_config["mandatory"]})

        keys_finded = [i["sheet_column"] for i in columns_to_return]
        config_names = [dict_config[i]['name'] for i in dict_config]

        for column_key in dict_config:
            column_name = dict_config[column_key]['name']

            if not column_name in keys_finded :
                raise Exception("The column corresponding to the key \"" + str(column_key) + " ( " + str(dict_config[column_key]['name'])  + " )\" in config.json was not found")

        return columns_to_return

    @staticmethod
    def import_data_dictionary(path, header=1, config=None):
        if config:
            Importer.config = config.parse()
            
        dict_config = Importer.config['dictionary']
        label_number = dict_config["header_line"] - 1

        excel = Importer.import_workbook(path)
        sheet_names = Importer.get_sheet_names_from_workbook(excel)

        sheets = {}

        ignored_reasons = {}

        for sheet_name in sheet_names:
            sheet_parsed = Importer.import_sheet_from_workbook(excel, sheet_name, header=label_number)

            if not sheet_name in dict_config["sheets"]:
                continue
            try:
	            clean_columns = Importer.clean_columns(sheet_parsed.columns, dict_config["columns"])
            except Exception as exception:
                print("The sheet ("+ sheet_name + ") could not be processed because of: " + exception.args[0] + "\n")
                continue

            sheet = Sheet(sheet_name, [])
            
            rows = sheet_parsed.get([i["sheet_column"] for i in clean_columns])

            for j, columns in enumerate(rows.values):
                row = list(columns)

                row_dict = {}
                include_row = True

                for i, column in enumerate(row):
                    row_dict[clean_columns[i]["column_key"]] = column

                    if type(column) == float and math.isnan(column) :
                        if clean_columns[i]["mandatory"]:
                            include_row = False
                            if clean_columns[1]["sheet_column"] not in ignored_reasons:
                                ignored_reasons[clean_columns[1]["sheet_column"]] = []

                            ignored_reasons[clean_columns[1]["sheet_column"]].append((j,sheet_name))
                            break                
                
                if include_row:
                    sheet.data.append(row_dict)
            
            # print(sheet.name,len(sheet.data))
            sheets[dict_config["sheets"][sheet_name]] = sheet
        print("Linhas ignoradas para as seguintes chaves configuradas como obrigatórias: ", ignored_reasons, "\n")
        
        return sheets

