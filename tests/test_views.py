from unittest.mock import patch

import pandas as pd

from src.views import greeting, load_operations_data, process_cards_data, get_top_transactions
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

def test_process_cards_data_empty():
    df = pd.DataFrame({})
    with pytest.raises(ValueError):
        process_cards_data(df)

def test_process_cards_data_missing_key():
    df_no_sum = pd.DataFrame({'Номер карты': ['1234']})
    with pytest.raises(KeyError, match="Отсутствуют колонки: Сумма операции"):
        process_cards_data(df_no_sum)

    df_no_card = pd.DataFrame({"Сумма операции": [100.00]})
    with pytest.raises(KeyError, match="Отсутствуют колонки: Номер карты"):
        process_cards_data(df_no_card)

    df_no_sum_card = pd.DataFrame({"other_column": [100.00]})
    with pytest.raises(KeyError, match="Отсутствуют колонки: Номер карты, Сумма операции"):
        process_cards_data(df_no_sum_card)

def test_process_cards_data_exception():
    df = pd.DataFrame({
        'Номер карты': ['1234567812345678'],
        'Сумма операции': [-100]
    })
    with patch('src.views.logger') as mock_logger:
        with patch('pandas.DataFrame.groupby') as mock_groupby:
            mock_groupby.side_effect = Exception("Критическая ошибка в process_cards_data")

            with pytest.raises(Exception, match="Критическая ошибка в process_cards_data"):
                process_cards_data(df)

            mock_logger.error.assert_called_once_with('Критическая ошибка в process_cards_data: Критическая ошибка в process_cards_data')

def test_process_cards_data():
    df = pd.DataFrame({
        'Номер карты': ['1234567812345678', '8765432187654321', '1234567812345678'],
        'Сумма операции': [-100.50, -200.75, -50.25]
    })

    result = process_cards_data(df)

    assert result is not None
    assert len(result) == 2

    assert result[0]['last_digits'] == '4321'
    assert result[0]['total_spent'] == 200.75
    assert result[0]['cashback'] == 2.01

    assert result[1]['last_digits'] == '5678'
    assert result[1]['total_spent'] == 150.75
    assert result[1]['cashback'] == 1.51

def test_get_top_transactions_none_empty():
    with pytest.raises(ValueError,  match="DataFrame не может быть None"):
        get_top_transactions(None)

    df_empty = pd.DataFrame()
    assert get_top_transactions(df_empty) == []


@pytest.mark.parametrize("columns_to_include, expected_error", [
    (['Сумма платежа', 'Категория', 'Описание'], "Дата операции"),
    (['Дата операции', 'Категория', 'Описание'], "Сумма платежа"),
    (['Дата операции', 'Сумма платежа', 'Описание'], "Категория"),
    (['Дата операции', 'Сумма платежа', 'Категория'], "Описание"),
    (['Дата операции', 'Сумма платежа'], "Категория, Описание"),
    (['Дата операции'], "Сумма платежа, Категория, Описание"),

])
def test_get_top_transactions_missing_columns(columns_to_include, expected_error):


    data = {col: ['test_value'] for col in columns_to_include}
    df = pd.DataFrame(data)

    with pytest.raises(KeyError, match=f"Отсутствуют обязательные колонки: {expected_error}"):
        get_top_transactions(df)

def test_get_top_transactions_invalid_top_n(valid_transactions_df):
    result = get_top_transactions(valid_transactions_df, top_n=-1)
    assert len(result) == 3

    result = get_top_transactions(valid_transactions_df, top_n=0)
    assert len(result) == 3

    result = get_top_transactions(valid_transactions_df, top_n=100)
    assert len(result) == 3

def test_get_top_transactions(valid_transactions_df):
    result = get_top_transactions(valid_transactions_df, top_n=2)
    assert len(result) == 2
    assert result == [{
                "date": '30.12.2021',
                "amount": 200.00,
                "category": 'Транспорт',
                "description": "Такси"},

                {"date": "31.12.2021",
                "amount": 100.00,
                "category": "Еда",
                "description": "Не указана"

            }]