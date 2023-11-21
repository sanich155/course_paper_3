import json
from unittest import mock

import pytest

from setttings import BASE_DIR
from src.utils import get_last_operations
from src.utils import hide_card_number


@pytest.fixture(autouse=True)
def mock_read_json():
    test_operations_path = BASE_DIR.joinpath('tests', 'test_operations.json')
    with test_operations_path.open(encoding='utf-8') as f:
        data = json.load(f)

    with mock.patch('src.utils.read_json') as mocked_object:
        mocked_object.return_value = data
        yield mocked_object


def test_hide_card_number():
    assert hide_card_number('Visa Gold 8326537236216459') == 'Visa Gold 8326 53** **** 6459'
    assert hide_card_number('MasterCard 6783917276771847') == 'MasterCard 6783 91** **** 1847'
    assert hide_card_number('Счет 17691325653939384901') == 'Счет 1769 13** **** 4901'


@pytest.mark.usefixtures('mock_read_json')
def test_get_last_operations():
    result = get_last_operations(0)
    assert result == []
