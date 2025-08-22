import json
import requests
from datetime import datetime, timedelta
import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_operations_data(path: str) -> pd.DataFrame|None:
    """Загружает данные операций из Excel-файла"""
    try:
        file_path = os.path.abspath(path)
        df = pd.read_excel(file_path, sheet_name='Отчет по операциям')
        logger.info(f'Данные успешно загружены, строк: {len(df)}')
        return df
    except FileNotFoundError:
        logger.error('Файл не найден')
        raise FileNotFoundError
    except TypeError:
        logger.error('Неверный формат значения')
        raise TypeError

def greeting() -> str:
    """Приветствует пользователя с учетом времени суток"""
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"
