'''main'''

import os
import json
from pathlib import Path
from code.product import Product
from code.transaction import Transaction
from datetime import datetime

PRODUCT_ARCHIVE_PATH = Path (__file__).parent / 'produtos.json'
LOG_TRANSACTIONS = Path(__file__).parent / 'transacoes.json'

def load_file(ARCHIVE_PATH):
    '''Load json from given path or create new, returns empty list'''
    if not os.path.exists(ARCHIVE_PATH):
        # If file does not exists, create new
        return []
    
    try:
        with open(ARCHIVE_PATH, 'r', encoding='utf8') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        # If file is empty or corrupted create new
        return []
    
def save_archive(ARCHIVE_PATH, data):
    '''Receives path and data and saves it as Json'''
    with open(ARCHIVE_PATH, 'w', encoding='utf-8') as file:
        # Ensure ascii false preserve characters
        json.dump(data, file, ensure_ascii=False, indent=2)

def add_class_to_list(object_, list_: list):
    '''Receives product class and returns list with new product in dict form'''
    list_.append (object_.__dict__)
    return list_

def clean_menu():
    '''Clean terminal; works on windows and linux/mac'''
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_main():
    '''Print options to users, returns option choosen (int)'''
    option = input(
        "[0] Salvar e sair\n"
        "[1] Adicionar novo produto\n"
        "[2] Retirar produto\n"
        "[3] Adicionar quantidade de produto existente\n"
    ).strip()
    try:
        option = int(option)
    except:
        return None
    return option

def menu_product_insertion():
    '''
    Asks user to input product indentification (id), quantity and own name, 
    returns values as tuples
    '''
    name = input(
        "Digite o nome do produto: \n"
    )
    quantity = input(
        "Digite a quantidade inicial: \n"
    )
    employee = input(
        "Quem está realizando esta transação? \n"
        "Digite seu nome abaixo: \n"
    )
    return name, quantity, employee

def menu_product_withdraw():
    '''
    Asks user to input product indentification (id), quantity and own name, 
    returns values as tuples
    '''
    id_ = input(
        "Informe o ID do produto que está retirando: \n"
    )
    quantity = input(
        "Informe a quantidade que está retirando: \n"
    ) 
    employee = input(
        "Quem está realizando esta transação? \n"
        "Digite seu nome abaixo: \n"
    )
    return id_, quantity, employee

def menu_product_update():
    '''
    Asks user to input product indentification (id), quantity and own name, 
    returns values as tuples
    '''
    id_ = input(
        "Informe o ID do produto que gostaria de atualizar: \n"
    )
    quantity = input(
        "Informe a quantidade que está acrescentando ao estoque: \n"
    ) 
    employee = input(
        "Quem está realizando esta transação? \n"
        "Digite seu nome abaixo: \n"
    )
    return id_, quantity, employee

def search_product(product_list: list, searched_id: int) -> dict | None:
    '''Search for id in list and return dict, if not found returns None'''
    for product in product_list:
        if product["id"]== searched_id:
            return product
    return None

def generate_id(list_):
        '''
        Generate new number considering last item on a list of dictionaries
        increased by 1, returns new number
        '''
        if not list_:
            return 1
        max_id_in_list = max(dictionary["id"] for dictionary in list_)
        return max_id_in_list + 1

def create_product(id_: int, name: str, quantity: int):
    '''Creates product using parameters'''
    return Product(id_, name, quantity)

def create_transaction(type, employee_name):
    '''
    Creates transaction of Transaction class and returns it. 
    Type 1 for updates, Type 2 for withdraws
    '''
    date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    match type:
        case "1":
            type = 'Abastecimento'
        case "2":
            type = 'Retirada' 
    return Transaction(type, date, employee_name)

def add_transaction(transaction_type, employee_name):
    '''
    Return list with new transaction added, transaction type 1 for adding, 2 for
    withdrawing
    '''
    transaction = create_transaction(transaction_type, employee_name)
    return add_class_to_list(transaction, transaction_list)

def register_transaction(new_transaction_list):
    '''
    Saves transaction to JSON log using updated list, returns success message 
    if succeded
    '''
    try:
        save_archive(LOG_TRANSACTIONS, new_transaction_list)
        message = 'Transação realizada com sucesso!'
    except Exception as e:
        # In future, could be more user friendly
        print('Erro ao tentar realizar transação: ', e)
        return
    return 'Transação realizada com sucesso!'

def validate_positive_int(value: str | int):
    '''Converts to positive integer. If possible returns value as int. If not
    returns False
    '''
    if isinstance(value, str):
        value = value.strip() 
    try:
        value = int(value)
    except:
        return False
    if value > 0:
        return value
    return False
    




message = None

# Loading from Json
product_list = load_file(PRODUCT_ARCHIVE_PATH)
transaction_list = load_file(LOG_TRANSACTIONS)

while True:

    clean_menu()
    if message is not None:
        print(message)
    option = menu_main()
    if option is None:
        break

    match option:

        case 1:
            # Add product
            clean_menu()
            id_ = generate_id(product_list)
            name, input_add_quantity, employee_name = menu_product_insertion()
            add_quantity = validate_positive_int(input_add_quantity)
            if not add_quantity:
                message = "Quantidade inválida"
                continue
            product = create_product(id_, name, add_quantity)
            new_product_list = add_class_to_list(
                product, product_list
                )
            save_archive(PRODUCT_ARCHIVE_PATH, new_product_list)
            new_transaction_list = add_transaction("1", employee_name)
            message = register_transaction(new_transaction_list)
            continue

        case 2:
            # Withdraw product
            clean_menu()
            input_id, input_withdraw_quantity, employee_name = menu_product_withdraw()
            id_ = validate_positive_int(input_id)
            withdraw_quantity = validate_positive_int(input_withdraw_quantity)
            print(product_list)
            data = search_product(product_list, id_)

            if data and id_ and withdraw_quantity:
                # Checks if withdraw amount is available in stocks
                if data["quantity"] >= withdraw_quantity:
                    data["quantity"] -= withdraw_quantity
                    save_archive(PRODUCT_ARCHIVE_PATH, product_list)
                else:
                    message = "Sem estoque para a transação"
                    continue
            else:
                message = "Erro ao realizar transação, confira se os valores " \
                "foram inseridos corretamente"
                continue
            new_transaction_list = add_transaction("2", employee_name)
            message = register_transaction(new_transaction_list)
            continue

        case 3:
            # Update existing product stocks
            clean_menu()
            input_id, input_update_quantity, employee_name = menu_product_update() 
            id_= validate_positive_int(input_id)
            update_quantity = validate_positive_int(input_update_quantity)
            data = search_product(product_list, id_)
            if data and update_quantity and id_:
                data["quantity"] += update_quantity
            else:
                message = "Erro ao realizar transação, confira se os valores " \
                "foram inseridos corretamente"
                continue
            new_transaction_list = add_transaction("1", employee_name)
            message = register_transaction(new_transaction_list)
            continue
                
        case 0:
            # Ends program, updates database through end of code
            break

        case _:
            # Else
            clean_menu()
            print(
                'Opção inválida'
                )
            
save_archive(PRODUCT_ARCHIVE_PATH, product_list)
save_archive(LOG_TRANSACTIONS, transaction_list)