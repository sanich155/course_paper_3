import datetime
import json
from pathlib import Path

from setttings import OPERATIONS_PATH
from src.models import Operation, OperationAmount, Currency


def read_json(file_path: Path) -> list[dict]:
    with file_path.open(encoding='utf-8') as f:  # pragma: no cover
        return json.load(f)


def take_operations() -> list[Operation]:
    operations_list = []
    for operation in read_json(OPERATIONS_PATH):
        if not operation:
            continue

        op = Operation(
            id=operation['id'],
            state=operation['state'],
            date=datetime.datetime.fromisoformat(operation['date']),

            operation_amount=OperationAmount(
                amount=float(operation['operationAmount']['amount']),
                currency=Currency(
                    name=operation['operationAmount']['currency']['name'],
                    code=operation['operationAmount']['currency']['code']
                )
            ),
            description=operation['description'],
            cart_from=operation.get('from'),
            cart_to=operation.get('to'),
        )
        operations_list.append(op)

    return operations_list


def hide_card_number(card_name_number: str) -> str:
    """Скрывает номер карты или счета"""

    *card_name_list, card_number = card_name_number.split()
    if card_name_list[0] == 'Счет':
        hidden_card_number = card_number[:4] + ' ' + card_number[4:6] + '**' + ' ' + '****' + ' ' + card_number[16:20]
    else:
        hidden_card_number = card_number[:4] + ' ' + card_number[4:6] + '**' + ' ' + '****' + ' ' + card_number[12:16]

    card_name = ' '.join(card_name_list)
    return f'{card_name} {hidden_card_number}'


def get_last_operations(count: int) -> list[Operation]:
    all_operations = take_operations()
    operations = filter(lambda op: op.state == 'EXECUTED', all_operations)
    return sorted(operations, reverse=True, key=lambda op: op.date)[:count]


def show_operations() -> None:
    """Выводит операции на экран в нужном формате"""

    for operation in get_last_operations(5):
        date_operation = operation.date.strftime('%d.%m.%Y')

        if operation.cart_from:
            card_name_from = hide_card_number(operation.cart_from)
        else:
            card_name_from = ''

        card_name_to = hide_card_number(operation.cart_to)

        print(f'{date_operation} {operation.description}\n'
              f'{card_name_from} -> {card_name_to}\n'
              f'{operation.operation_amount.amount} {operation.operation_amount.currency.name}\n')
