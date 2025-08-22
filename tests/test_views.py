from unittest.mock import patch

import pandas as pd

from src.views import greeting, load_operations_data
import pytest

@patch('src.views.datetime')
def test_greeting_morning(mock_datetime):
    mock_now = mock_datetime.now.return_value
    mock_now.hour = 7

    assert greeting() == "Доброе утро"

@patch('src.views.datetime')
def test_greeting_day(mock_datetime):
    mock_now = mock_datetime.now.return_value
    mock_now.hour = 14

    assert greeting() == "Добрый день"

@patch('src.views.datetime')
def test_greeting_evening(mock_datetime):
    mock_now = mock_datetime.now.return_value
    mock_now.hour = 21

    assert greeting() == "Добрый вечер"

@patch('src.views.datetime')
def test_greeting_night(mock_datetime):
    mock_now = mock_datetime.now.return_value
    mock_now.hour = 4

    assert greeting() == "Доброй ночи"

def test_load_operations_data_int():
    with pytest.raises(TypeError):
        load_operations_data(5)

def test_load_operations_data_no_file():
    with pytest.raises(FileNotFoundError):
        load_operations_data('no_file_at_all.xlsx')

@patch('pandas.read_excel')
@patch('os.path.abspath')
def test_load_operations_data(mock_abspath, mock_read_excel):
    mock_abspath.return_value = '\\fake\\path\\file.xlsx'
    mock_df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    mock_read_excel.return_value = mock_df

    result = load_operations_data('test.xlsx')
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2
    mock_read_excel.assert_called_once_with('\\fake\\path\\file.xlsx', sheet_name='Отчет по операциям')