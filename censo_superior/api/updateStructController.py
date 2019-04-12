from importer import Importer
from db.database import Database
from config import Config
from sheet import Sheet


class UpdateStructController:
    def __init__(self, db: Database, config: Config):
        self.db = db
        self.main_config = config
        self.__imported_dict = None

    def import_dict(self, path):
        self.__imported_dict = Importer.import_data_dictionary(
            path, config=self.main_config)
        return list(self.__imported_dict.keys())

    def parse(self, table):
        sheet: Sheet = self.__imported_dict[table]
        old_fields, old_fields_key = self.db.structure_dao.get_fields(
            table + Database.struct_suffix)
        diff_fields = []
        new_fields = [(data["name"], data["description"], data["type"])
                      for data in sheet.data]

        if old_fields and len(old_fields):
            # comparar campos e retornar as diferenças já eliminando os que possuem sinonimos

            for new_field in new_fields:
                is_new = True

                for old_field in old_fields:
                    synonymous = old_field[old_fields_key["synonymous"]].split(
                        ",")
                    field_type = old_field[old_fields_key["field_type"]]
                    ignore_field_import = old_field[old_fields_key["ignore_field_import"]]

                    if new_field[0] in synonymous:
                        if new_field[2].lower() != field_type.lower():
                            raise Exception(
                                "The field " + new_field[0] + "("+field_type+") already exists, but with a different type: " + new_field[2])
                        
                        is_new = False
                        break
                
                if is_new:
                    diff_fields.append(new_field)

        else:
            diff_fields = new_fields

        return diff_fields

        # return [campos novos]

    def save_table(self, table, field_dict):
        # return [campos novos] (somente os que deram erro)
        old_fields, old_fields_key = self.db.structure_dao.get_fields(
            table + Database.struct_suffix)
        errors = []
        if old_fields and len(old_fields):
            # verificar se algum sinonimo passado por parametro corresponde ao nome
            # de algum campo ao salvar, adicionar sinonimo na tabela struct
            pass
        else:
            self.db.structure_dao.add_fields(table, field_dict)

        return errors
