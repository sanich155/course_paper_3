from src.utils import show_operations
from src.utils import take_operations
from src.utils import hide_card_number
import json
import os

path_test = os.path.join('test_operations.json')


def test_show_operations():
    assert show_operations(path_test) is None


def test_take_operations():
    with open('test_operations.json', 'r', encoding='utf-8') as f:
        correct_test = json.load(f)
    assert take_operations(path_test) == correct_test


def test_hide_card_number():
    assert hide_card_number('Visa Gold 8326537236216459') == 'Visa Gold 8326 53** **** 6459'
    assert hide_card_number('MasterCard 6783917276771847') == 'MasterCard 6783 91** **** 1847'
    assert hide_card_number('Счет 17691325653939384901') == 'Счет 1769 13** **** 4901'
