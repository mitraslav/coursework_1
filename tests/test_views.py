from unittest.mock import patch
from src.views import greeting

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