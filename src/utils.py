import os
import json
import datetime

path = os.path.join('../operations.json')


def take_operations(path: str) -> list:
    """Возвращает список всех операций из *.json"""

    with open(path, 'r', encoding='utf-8') as f:
        all_operations = json.load(f)
    return all_operations


def hide_card_number(card_name_number: str) -> str:
    """Скрывает номер карты или счета"""

    card_name = ''
    for name in card_name_number.split():
        if name.isalpha():
            card_name += (name + ' ')
    if card_name == 'Счет ':
        card_number = card_name_number.split()[-1]
        hidden_card_number = (card_number[:4] + ' ' + card_number[4:6]
                              + '**' + ' ' + '****' + ' ' + card_number[16:20])
    else:
        card_number = card_name_number.split()[-1]
        hidden_card_number = (card_number[:4] + ' ' + card_number[4:6] + '**' + ' ' + '****' + ' ' + card_number[12:16])
    hidden_card = card_name + hidden_card_number
    return hidden_card


def show_operations(path: str) -> None:
    """Выводит операции на экран в нужном формате"""

    operations = []
    all_operations = take_operations(path)
    for operation in all_operations:
        if operation.get("state") == "EXECUTED":
            operations.append(operation)

    last_operations = sorted(operations, reverse=True,
                             key=lambda operation: operation['date'])[:5]

    for operation in last_operations:
        date_operation = datetime.datetime.strptime(operation.get("date"),'%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
        description = operation.get('description')

        if operation.get('from'):
            card_name_from = hide_card_number(operation.get('from'))
        else:
            card_name_from = ''

        card_name_to = hide_card_number(operation.get('to'))
        amount = operation.get('operationAmount').get('amount')
        currency_name = operation.get('operationAmount').get('currency').get('name')

        print(f'{date_operation} {description}\n'
              f'{card_name_from} -> {card_name_to}\n'
              f'{amount} {currency_name}\n')


show_operations(path)
