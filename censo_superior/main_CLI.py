from config import Config
from importer import Importer
from db.database import Database
from api.updateStructController import UpdateStructController
from os import path as os_path


def main_menu(controller):
    selection = -1
    print("========================= Menu Principal =========================\n")

    while selection < 0 or selection > 2:
        print("Selecione uma das ações abaixo:\n")
        print("\t0. Sair do programa\n")
        print("\t1. Importar nova estrutura\n")
        print("\t2. Importar dados para estrutura já existente\n")
        selection = int(input("Seleção (0,1,2): "))

    return selection


def importation_menu(table, updateController):
    fields_diff_map = []

    print("Buscando campos...")

    diff_fields = updateController.parse(table)

    for diff_field in diff_fields:  # diff_field = (name, description, type)
        fields_diff_map.append(
            {"name": diff_field[0], "description": diff_field[1], "synonymous": "", "import": True, "type": diff_field[2]})

    print("ok\n")

    while(True):
        selection = -1

        while selection < 0 or selection > 4:
            print("Selecione uma ação para a importação da tabela "+table+":\n")
            print("\t0. Sair\n")
            print("\t1. Voltar\n")
            print("\t2. Exibir quantidade de campos\n")
            print("\t3. Exibir campos (importados sem sinonimo encontrado)\n")
            print("\t4. Configurar campo\n")
            print("\t5. Salvar novos campos\n")
            selection = int(input("Seleção (0,1,2,3,4): "))

        if not selection:
            return 0
        elif selection == 1:
            return -1
        elif selection == 2:
            print("Quantidade de campos: " + str(len(fields_diff_map)))
        elif selection == 3:
            print("Nome", "Tipo", "Sinonimos", "Importar", "Descrição\n")

            for index, field in enumerate(fields_diff_map):
                print("#" + str(index + 1) + ".", "\"" + field["name"] + "\"", "\"" + field["type"] + "\"", "\"" +
                      field["synonymous"] + "\"", "\"" + str(field["import"]) + "\"", "\"" + field["description"].replace("\n", "\t") + "\"")

        elif selection == 4:
            field_index = -1

            while field_index < 1 or field_index > len(fields_diff_map):
                field_index = int(
                    input("Digite o índice do campo que deseja configurar: "))

            field = fields_diff_map[field_index - 1]

            field_action = -1
            print("\nCampo: #" + str(field_index) + ". ")
            print(field["name"], field["type"], field["synonymous"],
                  field["import"], field["description"] + "\n")

            while not field_action in [1, 2, 3]:
                print("Selecione uma ação para o campo:\n")
                print("\t1. Cancelar\n")
                print("\t2. Adicionar sinonimo\n")
                print(
                    "\t3. " + ("Importar" if not field["import"] else "Não importar") + "\n")
                field_action = int(input("Selecione (1,2,3):"))

            if field_action == 2:
                field["synonymous"] = input("Digite o sinonimo: ")
            elif field_action == 3:
                field["import"] = not field["import"]

        elif selection == 5:
            updateController.save_table(table, fields_diff_map)
            return -1


def import_structure(controller):
    print("========================= Importar nova estrutura =========================\n")

    exists_path = False

    while not exists_path:
        print("Importe um dicionário de dados\n")
        path = input("Caminho para o arquivo: ")
        exists_path = os_path.exists(path)

    updateController = UpdateStructController(
        controller["db"], config=controller["main_config"])

    imported_tables = updateController.import_dict(path)

    def choose_table(imported_tables):
        choosen_table = -1

        while choosen_table < 0 or choosen_table > len(imported_tables):
            print("Escolha uma das tabelas abaixo para trabalhar: \n")
            print("\t0. Sair\n")

            for index, imported_table in enumerate(imported_tables):
                print("\t" + str(index + 1) + ". " + imported_table + "\n")

            choosen_table = int(
                input("Selecione [0, " + str(len(imported_tables)) + "]: "))

        return choosen_table

    choosen_table = choose_table(imported_tables)

    while(choosen_table):
        print("========== Tabela " +
              imported_tables[choosen_table - 1] + " ==========\n")

        table_action = -1
        while not table_action in [0, 1, 2, 3]:
            print("Selecione uma ação: \n")
            print("\t0. Sair\n")
            print("\t1. Menu principal\n")
            print("\t2. Trocar tabela\n")
            print("\t3. Importar\n")
            table_action = int(input("Selecione(0,1,2,3): "))

        if not table_action:
            return table_action

        elif table_action == 1:
            return -1

        elif table_action == 2:
            choosen_table = choose_table(imported_tables)

        else:
            result = importation_menu(
                imported_tables[choosen_table - 1], updateController)

            if not result:
                choosen_table = result

    if not choosen_table:
        return 0

    return -1


if __name__ == "__main__":
    main_config = Config('config.json')
    db = Database(main_config.parse()[
                  "database_access"], main_config.parse()["censo_databases"])

    controller = {"path": "", "main_config": main_config, "db": db}
    menus = [main_menu, import_structure]
    menu_number = 0
    selection = -1

    print("Bem vindo ao importador de banco de dado Diplan censo, você está utilizando\n")
    print("interface de linha de comando (CLI)\n")
    print("Aperte (ctrl + c)/(ctrl + d) para interromper a aplicação\n")
    print("ou em algum menu pressione 0 para sair quando for permitido\n")

    while selection:
        selection = menus[menu_number](controller)

        if not selection:
            break
        elif selection == -1:
            menu_number = 0
        else:
            menu_number = selection

    print("Encerrando CLI...")