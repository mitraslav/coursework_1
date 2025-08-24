import functools
import json
import logging
from datetime import datetime
from typing import Callable, Optional

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def report_to_file(func: Optional[Callable] = None, *, filename: Optional[str] = None):
    """
    Декоратор для записи результатов функций-отчетов в файл.

    Args:
        func: Функция для декорирования (без параметра)
        filename: Имя файла для записи (с параметром)
    """

    def decorator(report_func):
        @functools.wraps(report_func)
        def wrapper(*args, **kwargs):
            try:
                # Выполняем функцию и получаем результат
                result = report_func(*args, **kwargs)

                # Определяем имя файла
                if filename:
                    output_filename = filename
                else:
                    # Генерируем имя файла по умолчанию
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    func_name = report_func.__name__
                    output_filename = f"{func_name}_report_{timestamp}.json"

                # Сохраняем результат в файл
                if isinstance(result, pd.DataFrame):
                    # Для DataFrame сохраняем в JSON
                    result.to_json(output_filename, orient="records", indent=2)
                elif isinstance(result, (dict, list)):
                    # Для словарей и списков сохраняем как JSON
                    with open(output_filename, "w", encoding="utf-8") as f:
                        json.dump(result, f, indent=2, ensure_ascii=False)
                else:
                    # Для других типов сохраняем как текст
                    with open(output_filename, "w", encoding="utf-8") as f:
                        f.write(str(result))

                logger.info(f"Отчет сохранен в файл: {output_filename}")
                return result

            except Exception as e:
                logger.error(f"Ошибка при создании отчета: {e}")
                raise

        return wrapper

    # Обработка вызова декоратора с параметрами или без
    if func is None:
        return decorator
    else:
        return decorator(func)


@report_to_file
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions: Датафрейм с транзакциями
        category: Название категории для анализа
        date: Опциональная дата (формат 'YYYY-MM-DD'). Если не указана, используется текущая дата.

    Returns:
        pd.DataFrame: Траты по категории за последние 3 месяца
    """
    try:
        # Проверяем входные данные
        if transactions.empty:
            logger.warning("Передан пустой датафрейм транзакций")
            return pd.DataFrame()

        # Определяем дату для анализа
        if date:
            analysis_date = pd.to_datetime(date)
        else:
            analysis_date = pd.to_datetime(datetime.now().date())

        # Вычисляем дату начала периода (3 месяца назад)
        start_date = analysis_date - pd.DateOffset(months=3)

        # Преобразуем даты в датафрейме к datetime
        transactions = transactions.copy()
        if "date" in transactions.columns:
            transactions["date"] = pd.to_datetime(transactions["date"])

        # Фильтруем транзакции по категории и дате
        category_mask = transactions["category"].str.lower() == category.lower()
        date_mask = (transactions["date"] >= start_date) & (transactions["date"] <= analysis_date)

        filtered_transactions = transactions[category_mask & date_mask].copy()

        if filtered_transactions.empty:
            logger.info(f"Не найдено транзакций по категории '{category}' за последние 3 месяца")
            return pd.DataFrame()

        # Группируем по месяцам и суммируем траты
        filtered_transactions["month"] = filtered_transactions["date"].dt.to_period("M")
        result = (
            filtered_transactions.groupby("month")
            .agg({"amount": "sum", "category": "count"})
            .rename(columns={"amount": "total_spent", "category": "transaction_count"})
        )

        result.reset_index(inplace=True)
        result["month"] = result["month"].astype(str)

        logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}'")
        return result

    except KeyError as e:
        logger.error(f"Отсутствует необходимая колонка в датафрейме: {e}")
        raise
    except Exception as e:
        logger.error(f"Ошибка при формировании отчета: {e}")
        raise
