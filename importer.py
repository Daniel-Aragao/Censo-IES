import csv
import pandas
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
    def import_sheet_from_workbook(workbook: pandas.io.excel.Excelfile, sheet_name, header=1):
        return workbook.parse(sheet_name, header=header)
    
    @staticmethod
    def import_sheet_columns(sheet: pandas.core.frame.DataFrame=None, path: str=None, sheet_name: str = None, header=1):
        if sheet:
            return sheet.columns
        else:
            return Importer.import_workbook(path).parse(sheet_name, header=header).columns
    
    @staticmethod
    def get_sheet_names_from_workbook(workbook: pandas.io.excel.Excelfile):
        return workbook.sheet_names

    @staticmethod
    def import_data_dictionary(path, header=1):
        dict_config = Importer.config.parse()['dictionary']

        excel = Importer.import_workbook(path)
        sheet_names = Importer.get_sheet_names_from_workbook(excel)

        sheets = {}

        for sheet_name in sheet_names:
            sheet_parsed = Importer.import_sheet_from_workbook(excel, sheet_name, header=1)

            sheet = {
                "name": sheet_name,
                "pandas_obj": sheet_parsed,
                "columns": list(sheet.columns),
                "data": []
            }

            # for column in sheet.columns:
            
            
            sheets.append(sheet)









