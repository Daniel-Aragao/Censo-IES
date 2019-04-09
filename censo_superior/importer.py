import csv
import pandas
import math
from sheet import Sheet
from config import Config


class Importer:
    config: Config = None

    @staticmethod
    def import_csv(path: str, delimiter: str ="|", encoding: str ='iso-8859-14', lines_limit: int = 0):
        lines = []
        count = 0

        with open(path, encoding='iso-8859-14') as file_obj_control:
            reader = csv.DictReader(file_obj_control, delimiter=delimiter)
            
            for row in reader:
                lines.append(row)
                
                count += 1 
                if lines_limit and count >= lines_limit:
                    break
        
        return lines

    @staticmethod
    def import_workbook(path):
        return pandas.ExcelFile(path)

    @staticmethod
    def import_sheet_from_workbook(workbook: pandas.io.excel.ExcelFile, sheet_name, header=1):
        return workbook.parse(sheet_name, header=header)
    
    @staticmethod
    def import_sheet_columns(sheet: pandas.core.frame.DataFrame=None, path: str=None, sheet_name: str = None, header=1):
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

                if new_column.find(column_config["name"].upper()) >= 0:
                    columns_to_return.append({"sheet_column": new_column, "column_key": column_key, "mandatory": column_config["mandatory"]})

        return columns_to_return

    @staticmethod
    def import_data_dictionary(path, header=1, config=None):
        if config:
            Importer.config = config.parse()
            
        dict_config = Importer.config['dictionary']
        label_number = dict_config["header_line"]

        excel = Importer.import_workbook(path)
        sheet_names = Importer.get_sheet_names_from_workbook(excel)

        sheets = {}

        for sheet_name in sheet_names:
            sheet_parsed = Importer.import_sheet_from_workbook(excel, sheet_name, header=label_number)

            if not sheet_name in dict_config["sheets"]:
                continue
            
            clean_columns = Importer.clean_columns(sheet_parsed.columns, dict_config["columns"])

            sheet = Sheet(sheet_name, [])
            
            rows = sheet_parsed.get([i["sheet_column"] for i in clean_columns])

            for columns in rows.values:
                row = list(columns)

                row_dict = {}
                include_row = True

                for i, column in enumerate(row):
                    row_dict[clean_columns[i]["column_key"]] = column

                    if type(column) == float and math.isnan(column) :
                        if clean_columns[i]["mandatory"]:
                            include_row = False
                            break
                
                
                if include_row:
                    sheet.data.append(row_dict)            
            
            sheets[dict_config["sheets"][sheet_name]] = sheet
        
        return sheets

