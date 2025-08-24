import json
import requests
from datetime import datetime
import pandas as pd
import os
import logging
from dotenv import load_dotenv

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


def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> list[dict]|None:
    """Получение топ-N транзакций по сумме платежа"""
    if df is None:
        logger.error("Передан None вместо DataFrame")
        raise ValueError("DataFrame не может быть None")

    if df.empty:
        logger.warning("Передан пустой DataFrame")
        return []

    required_columns = ['Дата операции', 'Сумма платежа', 'Категория', 'Описание']
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        error_msg = f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}"
        logger.error(error_msg)
        raise KeyError(error_msg)

    if top_n <= 0:
        logger.warning(f"Некорректное значение top_n: {top_n}. Установлено значение по умолчанию: 5")
        top_n = 5
    try:
        df_copy = df.copy()
        df_copy['date_formatted'] = pd.to_datetime(df_copy['Дата операции']).dt.strftime('%d.%m.%Y')


        top_transactions = df_copy.nlargest(top_n, 'Сумма платежа', keep='all')

        result = []
        for _, row in top_transactions.iterrows():
            result.append({
                "date": row['date_formatted'],
                "amount": round(row['Сумма платежа'], 2),
                "category": row['Категория'] if pd.notna(row['Категория']) else "Не указана",
                "description": row['Описание'] if pd.notna(row['Описание']) else "Не указана"
            })
        logger.info(f"Успешно обработано {len(result)} транзакций из {top_n} запрошенных")
        return result
    except Exception as e:
        logger.error(f"Критическая ошибка в get_top_transactions: {e}")
        raise

def get_currency_rates(user_set_path: str) -> list[dict]|None:
    """Получение курсов валют через API"""
    try:

        load_dotenv('..\\.env')
        api_key = os.getenv('API_KEY_CURR')

        if not api_key:
            raise ValueError('API ключ не найден')


        abs_path = os.path.abspath(user_set_path)
        with open(abs_path) as file:
            user_currencies = json.load(file).get('user_currencies')

        if not user_currencies:
            logger.info("Нет выбранных валют в настройках")
            return []

        rates = []

        for currency in user_currencies:

            url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount=1"
            headers = {"apikey": api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()

            if 'result' in result:
                curr_rate = result['result']
                rates.append({
                    "currency": currency,
                    "rate": round(curr_rate, 2)
                })
            else:
                logger.warning(f"Не удалось получить курс для {currency}: {result}")


        return rates
    except FileNotFoundError:
        logger.error(f"Файл настроек не найден: {user_set_path}")
        raise FileNotFoundError


def get_stock_prices() -> list[dict]:
    """Получение цен акций (заглушка)"""

    pass
