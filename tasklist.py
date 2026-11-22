import json  # biblioteca para uso de arquivos JSON
import os
import re
from datetime import datetime  # biblioteca para manipulação de datas
from pathlib import Path

LIST_NAME = "Lista de Tarefas"
COMMON_WORDS = ["de", "da", "do", "das", "dos"]
FILE_EXT = ".json"
FILE_NAME = LIST_NAME.replace(" ", "_")
FILE_NAME = re.sub('[^A-Za-z0-9_-]+', '', FILE_NAME)
FILE_NAME = FILE_NAME.lower() + FILE_EXT
DATA_FILE = Path.home() / 'Documents' / 'tasklist_data' / FILE_NAME
MENU = [
    "Adicionar Tarefa",
    "Listar Tarefas",
    "Marcar como Concluída",
    "Remover Tarefas",
    "Sair",
]


def main():
    task_list = load_tasks()
    if task_list is None:
        main_loop = False
    else:
        main_loop = True
    while main_loop:
        print("=================================")
        print("Gerenciador de Tarefas")
        print("=================================")

        interaction = verify_data(MENU, "menu")

        match interaction:
            case 1:
                add_task(task_list)
            case 2:
                list_tasks(task_list)
            case 3:
                interaction = verify_data(task_list, "complete")
                if interaction is None:
                    continue
                complete_task(interaction, task_list)
            case 4:
                interaction = verify_data(task_list, "remove")
                if interaction is None:
                    continue
                remove_task(interaction, task_list)
            case 5:
                print("Encerrando o programa...")
                main_loop = False


def find_list_file():
    try:
        file_path = DATA_FILE
        with open(file_path, 'r', encoding="utf-8") as read_data:
            list_data = json.load(read_data)
        return list_data
    except OSError as e:
        print(f"Erro ao ler o arquivo: {e}")
        user_choice = input("Deseja continuar com uma nova lista? (S/N) ")
        if user_choice.lower() == 's':
            return create_list_file()
        else:
            print("Operação cancelada. Nenhum arquivo foi criado. O sistema será encerrado.")
            return None


def create_list_file():
    global FILE_NAME
    global DATA_FILE
    list_name = input("Digite o nome que deseja para a nova lista (ex: Afazeres Domésticos): ")
    file_name = list_name.replace(" ", "_")
    file_name = re.sub('[^A-Za-z0-9_-]+', '', file_name)
    file_name = file_name.lower() + FILE_EXT
    FILE_NAME = file_name
    DATA_FILE = Path.home() / 'Documents' / 'tasklist_data' / FILE_NAME
    list_data = []
    save_tasks(list_data)
    print(f"Novo arquivo de tarefas criado em: {DATA_FILE}")
    return list_data


def system_action():
    user_choice = input("A lista padrão não foi encontrada. Deseja criar uma nova lista de tarefas? (S/N) ")
    if user_choice.lower() == 's':
        return create_list_file()
    else:
        print("Operação cancelada. Nenhum arquivo foi criado.")
        return None


def load_tasks():
    global FILE_NAME
    global DATA_FILE
    if os.path.exists(DATA_FILE):
        return find_list_file()
    else:
        return system_action()
    return list_data


def show_menu():
    for i, item in enumerate(MENU):
        print(f"{i + 1}. {item}")


def verify_data(area, objective):
    menu_loop = True
    while menu_loop:
        match objective:
            case "complete":
                list_tasks(area)
                interaction = input(
                    "Digite o ID da tarefa que deseja marcar como concluída (ou 0 para cancelar): "
                )
            case "remove":
                list_tasks(area)
                interaction = input(
                    "Digite o ID da tarefa que deseja remover (ou 0 para cancelar): "
                )
            case _:
                show_menu()
                interaction = input(
                    "Digite o número da opção desejada: "
                )
        if (interaction.isdigit()) and (interaction.strip() != ""):
            interaction = int(interaction)
            if 1 <= interaction <= len(area):
                menu_loop = False
                return interaction
            elif interaction == 0:
                print("Operação cancelada.\n")
                menu_loop = False
                return None
        print("Entrada inválida. Por favor, escolha entre os números exibidos no menu.\n")


def save_tasks(task_list):
    file_path = DATA_FILE
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as write_data:
        json.dump(
            task_list, write_data, sort_keys=True, indent=4, ensure_ascii=False
        )  # salva a nova lista de tarefas no arquivo JSON


def add_task(task_list):
    menu_loop = True
    while menu_loop:
        description = input("Digite a descrição da tarefa (ou 0 para cancelar): ")
        if description.isdigit():
            description = int(description)
            if description == 0:
                print("Operação cancelada.\n")
                menu_loop = False
            else:
                print(f"Entrada inválida. '{description}' não é um valor válido para a descrição da tarefa.\n")
        elif description.strip() == "":
            print(f"Entrada inválida. '{description}' não é um valor válido para a descrição da tarefa.\n")
        else:
            menu_loop = False
    today = datetime.today().strftime(
        "%Y-%m-%d"
    )  # recebe a data atual formatada no exato momento em que o usuário adicionar a tarefa.
    task = {
        "id": len(task_list) + 1,
        "description": description,
        "concluded": False,
        "created_at": today,
    }
    task_list.append(task)
    save_tasks(task_list)
    print("Tarefa adicionada com sucesso!\n")


def list_tasks(task_list):
    print("Lista de Tarefas:")
    if not task_list:
        print("Nenhuma tarefa encontrada.\n")
    else:
        for task in task_list:
            status = "Concluída" if task["concluded"] else "Pendente"
            print(
                f"{task['id']}. {task['description']} - {status} (Criada em: {task['created_at']})"
            )


def complete_task(task_id, task_list):
    for task in task_list:
        if task["id"] == task_id:
            task["concluded"] = True
            save_tasks(task_list)
            print(f"Tarefa {task_id} marcada como concluída.")
            return
    print(f"Tarefa {task_id} não encontrada.\n")


def remove_task(task_id, task_list):
    new_list = []
    i = 0
    for task in task_list:
        if task["id"] == int(task_id):
            pass
        else:
            task["id"] = i + 1
            i += 1
            new_list.append(task)
    save_tasks(new_list)
    print(f"Tarefa {task_id} removida com sucesso.\n")


main()