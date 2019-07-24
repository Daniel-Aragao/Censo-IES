import time

from importer import Importer
from db.database import Database
from config import Config
from sheet import Sheet


class UpdateStructController:
    def __init__(self, db, config):
        self.db = db
        self.main_config = config
        self.__imported_dict = None

    def import_dict(self, path):
        """
        Receiving a path brings a dictionary sheet for memory to make any work
        """
        self.__imported_dict = Importer.import_data_dictionary(
            path, config=self.main_config)
            
        return list(self.__imported_dict.keys())

    def parse(self, table):
        """
        After importing a dictionary from a sheet (function import_dict) do:

        Receiving a table name it brings the actual diferrence betwen the given sheet
        and the fields already saveded, returning a list of tuples of fields not
        present in the synonymous column with the format ahead:

        return [(name, description, type)]

        obs.: The table name does not include suffixes _struct or _data
        """
        table = table.lower()
        sheet = self.__imported_dict[table]
        
        old_fields, old_fields_key = self.db.structure_dao.get_fields(
            table + Database.struct_suffix)
            
        new_fields = [[data["name"], data["description"], data["type"], ""]
                      for data in sheet.data]
                      
        diff_fields = []

        if old_fields and len(old_fields):
            for new_field in new_fields:
                is_new = True

                for old_field in old_fields:
                    synonymous = old_field[old_fields_key["synonymous"]].split(",")
                    description = old_field[old_fields_key["field_description"]]
                    field_type = old_field[old_fields_key["field_type"]]
                    ignore_field_import = old_field[old_fields_key["ignore_field_import"]]

                    if new_field[0].strip() in synonymous:
                        if new_field[2].lower() != field_type.lower():
                            raise Exception(
                                "The field " + new_field[0] + "("+field_type+") already exists, but with a different type: " + new_field[2])

                        is_new = False
                        break 
                    
                    elif description.lower().strip() == new_field[1].lower().strip():
                        new_field[3] = old_field[old_fields_key["field_name"]]

                if is_new:
                    diff_fields.append(new_field)

        else:
            diff_fields = new_fields

        return diff_fields

    def save_table(self, table, fields_dicts):
        """
        Gets the table name and the field fields_dicts, in the format bellow, and save in the database
        the new fields in <table>_struct and update the columns in <table>_data, but only if all
        the synonymous informed were encountered as a field name in <table>_struct.

        Obs.:
            table name: The table name does not include suffixes _struct or _data
            field_dict: [{"name":<str>, "description": <str>, "synonymous": <str>, "import": <boolean>, "type": <str>}]
        """
        table = table.lower()
        # return [campos novos] (somente os que deram erro)
        old_fields, old_fields_key = self.db.structure_dao.get_fields(
            table + Database.struct_suffix)

        errors = []

        new_fields = []
        new_synonym = []

        time_now = time.strftime('%Y-%m-%d %H:%M:%S')

        if old_fields and len(old_fields):
            for field_dict in fields_dicts:
                synonym = field_dict["synonymous"]

                if synonym:
                    try:
                        updated_id = next(
                            old_field[old_fields_key["id"]] for old_field in old_fields if old_field[old_fields_key["field_name"]] == synonym)

                        new_synonym.append((field_dict["name"], time_now, field_dict["imported_year"], updated_id))

                    except StopIteration as e:
                        errors.append(field_dict)

                else:
                    if field_dict["import"]:
                        new_fields.append(field_dict)

        else:
            new_fields = fields_dicts

        if not len(errors):
            self.db.structure_dao.add_fields(table, new_fields)
            self.db.structure_dao.update_synonym(table, new_synonym)

        return errors
