import pytest
import pandas as pd

@pytest.fixture
def valid_transactions_df():
    return pd.DataFrame({
        'Дата операции': ['31.12.2021 16:44:00', '30.12.2021 17:50:17', '24.12.2021 18:18:27'],
        'Сумма платежа': [100.0, 200.0, 50.0],
        'Категория': ['Еда', 'Транспорт', 'Развлечения'],
        'Описание': [None, 'Такси', 'Кино']
    })

TEST_USER_SETTINGS = {
    "user_currencies": ["USD", "EUR"],
    "user_stocks": ["AAPL", "GOOGL"]
}

TEST_API_RESPONSE = {
    "success": True,
    "result": 75.45
}