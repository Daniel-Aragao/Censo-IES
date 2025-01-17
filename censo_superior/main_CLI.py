from config import Config
from importer import Importer
from db.database import Database
from api.updateStructController import UpdateStructController
from api.importDataController import ImportDataController

from log import log_printer

from os import path as os_path
import time

def select_option(text, options, start=0):
    selection = -1
    qtd_opts = len(options)
    
    while start > selection or selection > qtd_opts:
        print(text,'\n')
        
        for i, option in enumerate(options):
            print("\t" + str(i + start) + ".", option, "\n")
        
        selection = input("Seleção [" + str(start) + ", " + str(qtd_opts - 1 + start ) + "]: ")
        
        try:
            selection = int(selection)
        except:
            selection = -1
    
    return selection
    

def main_menu(controller):
    print("========================= Menu Principal =========================\n")
    
    selection = select_option("Selecione uma das ações abaixo:",
    [
        "Sair do programa",
        "Importar nova estrutura",
        "Importar dados para estrutura já existente"
    ])
    
    return selection


def importation_menu(table, updateController):
    fields_diff_map = []

    print("Buscando campos...")

    diff_fields = updateController.parse(table)
    
    for diff_field in diff_fields:  # diff_field = (name, description, type)
        fields_diff_map.append(
            {"name": diff_field[0], "description": diff_field[1], "synonymous": diff_field[3], "import": True, "type": diff_field[2]})

    while(True):
        selection = -1
        
        selection = select_option("Selecione uma ação para a importação da tabela ("+table+"):",
        [
            "Sair",
            "Voltar",
            "Exibir quantidade de campos novos",
            "Exibir campos Novos",
            "Exibir campos Novos (SEM sinonimo)",
            "Configurar campo",
            "Salvar novos campos e finalizar operação"
        ])

        if not selection:
            return 0
        elif selection == 1:
            return -1
        elif selection == 2:
            print("Quantidade de campos: " + str(len(fields_diff_map)))
        elif selection == 3 or selection == 4:
            print("Ordem dos valores\nNome", "Tipo", "Sinonimos", "Importar", "Descrição\n")
            print("----------------------------------------------------------------------\n")
            
            for index, field in enumerate(fields_diff_map):
                if selection == 4 and field["synonymous"]:
                    continue
                    
                print("#" + str(index + 1) + ".", "\"" + field["name"] + "\"", "\"" + field["type"] + "\"", "\"" +
                      field["synonymous"] + "\"", "\"" + str(field["import"]) + "\"", "\"" + field["description"].replace("\n", "\t") + "\"")
                print("----------------------------------------------------------------------\n")
        
        elif selection == 5:
            if len(fields_diff_map) > 0:
                field_index = -1
    
                while field_index < 1 or field_index > len(fields_diff_map):
                    aux = input("Digite o índice do campo que deseja configurar [1, " + str(len(fields_diff_map)) + "]: ")
                
                    if aux:
                        try:
                            field_index = int(aux)
                        except:
                            pass
    
                field = fields_diff_map[field_index - 1]
    
                field_action = -1
                print("\nCampo: #" + str(field_index) + ". ")
                print(field["name"], field["type"], field["synonymous"],
                      field["import"], field["description"] + "\n")
                      
                field_action = select_option("Selecione uma ação para o campo:",
                [
                    "Cancelar",
                    "Adicionar sinônimo",
                    ("Importar" if not field["import"] else "Não importar")
                ], start=1)
    
                if field_action == 2:
                    field["synonymous"] = input("Digite o sinonimo: ")
                elif field_action == 3:
                    field["import"] = not field["import"]

        elif selection == 6:
            selection = -1
            
            qtd_synonymous = len([i for i in fields_diff_map if i["synonymous"]])
            qtd_news = len(fields_diff_map) - qtd_synonymous
            
            text = "Você tem certeza que deseja finalizar e salvar todos os campos?"
            text += "\n==> Campos configurados como sinônimos: " + str(qtd_synonymous)
            text += "\n==> Campos configurados como novos:     " + str (qtd_news)
            
            selection = select_option(text,
            [
                "Finalizar e salvar",
                "Voltar"
            ], start=1)
            
            if selection == 1:
                imported_year = 0

                while (imported_year < 1000 or imported_year > 9999):
                    try:
                        imported_year = int(input("O ano do dicionário a ser importado (4 dígitos): "))
                    except:
                        print("Valor inválido")

                for field in fields_diff_map:
                    field["imported_year"] = imported_year

                errors = updateController.save_table(table, fields_diff_map)

                if not len(errors):
                    return -1
                else:
                    print("\nErro(s) encontrado(s) no(s) campo(s)")
                    print("Ordem dos valores\nNome", "Tipo", "Sinonimos", "Importar", "Descrição\n")
                    
                    for field in errors:
                        field_index = fields_diff_map.index(field) + 1

                        print("\nCampo: #" + str(field_index) + ". ")
                        print(field["name"], field["type"], field["synonymous"],
                            field["import"], field["description"] + "\n")
                    
                    print("Verificar se os sinônimos configurados estão corretos")

                    selection = -1
            elif selection == 2:
                selection = -1


def import_structure(controller):
    print("========================= Importar nova estrutura =========================\n")

    exists_path = False

    while not exists_path:
        print("Importe um dicionário de dados\n")
        path = input("Caminho para o arquivo: ")
        exists_path = os_path.exists(path)
                
        if not exists_path:
            print("Caminho inválido")

    updateController = UpdateStructController(
        controller["db"], config=controller["main_config"])

    imported_tables = updateController.import_dict(path)

    def choose_table(imported_tables):
        opts = ["Sair"]
        
        for imported_table in imported_tables:
            opts.append(imported_table)
        
        choosen_table = select_option("Escolha uma das tabelas abaixo para trabalhar:", opts)

        return choosen_table

    choosen_table = choose_table(imported_tables)

    while(choosen_table):
        print("========== Tabela (" +
              imported_tables[choosen_table - 1] + ") ==========\n")

        table_action = select_option("Selecione uma ação:", ["Sair", "Menu principal", "Trocar tabela", "Importar"])

        if not table_action:
            return table_action

        elif table_action == 1:
            return -1

        elif table_action == 2:
            choosen_table = choose_table(imported_tables)

        else:
            result = importation_menu(imported_tables[choosen_table - 1], updateController)

            if not result:
                choosen_table = result

    if not choosen_table:
        return 0

    return -1
    
def chose_data_table_menu(db):
    not_created_tables_names, created_tables_names = db.get_existent_data_table()
    selection = -1
    
    opts = []
    
    for table_name in created_tables_names:
        opts.append(table_name)
    
    selection = select_option("Selecione uma das tabelas abaixo para importar:", ["Menu principal"] + opts)
    
    if not selection:
        return 0
    
    return created_tables_names[selection - 1]
        

def import_data(controller):
    print("========================= Importar novos dados =========================\n")
    
    choosen_table_name = chose_data_table_menu(controller["db"])
    
    if(choosen_table_name):
        selection = -1
        
        text = "========== Tabela (" + choosen_table_name + ") ==========\n"
        text += "Selecione uma das ações abaixo:"
        
        selection = select_option(text, ["Sair do programa", "Menu principal", "Importar dados"])
        
        if not selection:
            return 0
        elif selection == 1:
            return -1
        elif selection == 2:
            exists_path = False
        
            while not exists_path:
                print("Importe um conjunto de dados\n")
                path = input("Caminho para o arquivo: ")
                exists_path = os_path.exists(path)
                
                if not exists_path:
                    print("Caminho inválido")

            import_year = 0

            while (import_year < 1000 or import_year > 9999):
                try:
                    import_year = int(input("O ano do dicionário do dado a ser importado (4 dígitos): "))
                except:
                    print("Valor inválido")
        
            importDataController = ImportDataController(
                controller["db"], config=controller["main_config"], path=path, table_name=choosen_table_name, import_year=import_year)

            log_name = str(choosen_table_name) + " from " + str(import_year)
            
            log_printer("Iniciando importação..." + log_name,log_name)
            log_printer("Obs.: Quanto maior o arquivo mais lenta sua importação",log_name)
            start_time = time.time()

            try:
                importDataController.import_data()
                minutes = (time.time() - start_time) / 60
                log_printer("Finalizando importação com SUCESSO... em " + str(minutes) + " minutos", log_name)
            except Exception as ex:
                # trackeback.print
                minutes = (time.time() - start_time) / 60
                print(ex)
                log_printer("Finalizando importação com FALHA... em " + str(minutes) + " minutos", log_name)
            
    return -1


if __name__ == "__main__":
    main_config = Config('config.json')
    db = Database(main_config.parse()["database_access"], main_config.parse()["censo_databases"])

    controller = {"path": "", "main_config": main_config, "db": db}
    menus = [main_menu, import_structure, import_data]
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
