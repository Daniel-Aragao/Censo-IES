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
    def clean_columns(columns, columns_to_read):
        clean_columns = list(filter(lambda x: str(x).lower().find("unnamed") < 0, list(columns)))
        clean_columns = list(map(lambda x: str(x).replace("\n",'').upper(), clean_columns))

        columns_to_read = [i["name"] for i in columns_to_read]

        return list(filter(lambda x: x in columns_to_read, clean_columns))

    @staticmethod   
    def __is_mandatory(column, columns_to_read):
        for column_to_read in columns_to_read:
            
            name = column_to_read["name"].upper()
            column_upper = column.upper()

            if column_upper.find(name) >= 0 or name.find(column_upper) >= 0:
                return column_to_read["mandatory"]

    @staticmethod
    def import_data_dictionary(path, header=1, config=None):
        if config:
            Importer.config = config
            
        dict_config = Importer.config['dictionary']
        label_number = dict_config["header_line"]
        columns_to_read = dict_config["columns"].values()
        columns_keys = list(dict_config["columns"].keys())


        excel = Importer.import_workbook(path)
        sheet_names = Importer.get_sheet_names_from_workbook(excel)

        sheets = {}

        for sheet_name in sheet_names:
            sheet_parsed = Importer.import_sheet_from_workbook(excel, sheet_name, header=label_number)

            if not sheet_name in dict_config["sheets"]:
                continue
            
            clean_columns = Importer.clean_columns(sheet_parsed.columns, columns_to_read)

            sheet = Sheet(sheet_name, [])
            # sheet = {
            #     "name": sheet_name,
            #     "pandas_obj": sheet_parsed,
            #     "columns": clean_columns,
            #     "data": []
            # }
            
            rows = sheet_parsed.get(clean_columns)

            for columns in rows.values:
                row = list(columns)

                row_dict = {}
                include_row = True

                for i, column in enumerate(row):
                    clean_columns[i] era para ser na verdade as chaves do dicionario columns
                    row_dict[clean_columns[i]] = column

                    if type(column) == float and math.isnan(column) :
                        if Importer.__is_mandatory(clean_columns[i], columns_to_read):
                            include_row = False
                            break
                
                
                if include_row:
                    sheet.data.append(row_dict)            
            
            sheets[dict_config["sheets"][sheet_name]] = sheet
        
        return sheets

