import json
import requests
from datetime import datetime
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

def process_cards_data(df: pd.DataFrame) -> list[dict]|None:
    """Обработка данных по картам"""
    cards_data = []

    try:
        if df is None or df.empty:
            logger.warning("Передан пустой DataFrame")
            raise ValueError

        required_columns = ['Номер карты', 'Сумма операции']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            error_msg = f"Отсутствуют колонки: {', '.join(missing_columns)}"
            logger.error(error_msg)
            raise KeyError(error_msg)


        expense_df = df[(df['Сумма операции'] < 0) & (df['Номер карты'].notna())].copy()
        expense_df['last_digits'] = expense_df['Номер карты'].str[-4:]

        for card_digits, group in expense_df.groupby('last_digits'):
            total_spent = abs(group['Сумма операции'].sum())
            cashback = total_spent * 0.01

            cards_data.append({
                "last_digits": card_digits,
                "total_spent": round(total_spent, 2),
                "cashback": round(cashback, 2)
            })

        cards_data.sort(key=lambda x: x['total_spent'], reverse=True)
        logger.info(f'Обработано {len(cards_data)} карт"')
        return cards_data

    except (ValueError, KeyError) as e:
        logger.error(f'Ошибка в process_cards_data: {e}')
        raise
    except Exception as e:
        logger.error(f'Критическая ошибка в process_cards_data: {e}')
        raise
