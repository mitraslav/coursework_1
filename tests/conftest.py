import pandas as pd
import pytest


@pytest.fixture
def valid_transactions_df():
    return pd.DataFrame(
        {
            "Дата операции": ["31.12.2021 16:44:00", "30.12.2021 17:50:17", "24.12.2021 18:18:27"],
            "Сумма платежа": [100.0, 200.0, 50.0],
            "Категория": ["Еда", "Транспорт", "Развлечения"],
            "Описание": [None, "Такси", "Кино"],
        }
    )


TEST_USER_SETTINGS = {"user_currencies": ["USD", "EUR"], "user_stocks": ["AAPL", "GOOGL"]}

TEST_API_RESPONSE = {"success": True, "result": 75.45}

TEST_MARKETSTACK_RESPONSE = {"data": [{"close": 150.456, "symbol": "AAPL", "exchange": "XNAS"}]}

TEST_EXCHANGERATE_RESPONSE = {"result": 11250.75, "success": True}


@pytest.fixture
def test_data():
    """Создает тестовый DataFrame с различными датами"""
    data = {
        "Дата операции": [
            "01.01.2024 10:00:00",  # Начало месяца
            "15.01.2024 14:30:00",  # Середина месяца
            "31.01.2024 23:59:59",  # Конец месяца
            "01.02.2024 00:00:00",  # Следующий месяц
            "31.12.2023 23:59:59",  # Предыдущий год
            "invalid_date",  # Некорректная дата
            "15.01.2024 09:15:00",  # Еще одна дата в пределах месяца
        ],
        "Сумма": [100, 200, 300, 400, 500, 600, 700],
        "Описание": ["оп1", "оп2", "оп3", "оп4", "оп5", "оп6", "оп7"],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_operations():
    return [
        {"Категория": "Переводы", "Описание": "Валерий А."},
        {"Категория": "Переводы", "Описание": "Сергей З."},
        {"Категория": "Переводы", "Описание": "ООО Рога и копыта"},
        {"Категория": "Супермаркеты", "Описание": "Магнит"},
        {"Категория": "Переводы", "Описание": "Артем П."},
        {"Категория": "Переводы", "Описание": "Иван С."},
    ]


@pytest.fixture
def sample_transactions():
    """Создает тестовый датафрейм с транзакциями."""
    dates = pd.date_range(start="2024-01-01", end="2024-04-15", freq="D")
    data = []

    for date in dates:
        # Транзакции по разным категориям
        data.append({"date": date, "category": "Food", "amount": 100.0})
        data.append({"date": date, "category": "Transport", "amount": 50.0})
        if date.day % 7 == 0:  # Раз в неделю
            data.append({"date": date, "category": "Entertainment", "amount": 200.0})

    return pd.DataFrame(data)
