import json
from typing import Any, Dict

from src.utils import (filter_data_by_month_range, get_currency_rates, get_stock_prices, get_top_transactions,
                       greeting, load_operations_data, logger, process_cards_data)


def main_function(input_time: str, file_path: str = "..\\files\\operations.xlsx") -> str:
    """
    Главная функция, возвращающая JSON-ответ
    """
    try:
        # Загрузка данных
        df = load_operations_data(file_path)
        if df.empty:
            return json.dumps({"error": "Не удалось загрузить данные"}, ensure_ascii=False)

        logger.info(f"Загружено {len(df)} записей")
        logger.info(f"Колонки: {df.columns.tolist()}")

        if "Дата операции" in df.columns:
            logger.info(f"Примеры дат: {df['Дата операции'].head(3).tolist()}")

        # Фильтрация данных
        filtered_df = filter_data_by_month_range(df, input_time)

        logger.info(f"После фильтрации: {len(filtered_df)} записей")

        if filtered_df.empty:
            logger.warning("Нет данных после фильтрации. Проверяем возможные причины...")

            # Диагностика
            if "Дата операции" in df.columns:
                unique_dates = df["Дата операции"].unique()
                logger.info(f"Уникальные даты в исходных данных: {unique_dates[:10]}")  # первые 10

                # Проверяем диапазон дат в данных
                if hasattr(df["Дата операции"], "min") and hasattr(df["Дата операции"], "max"):
                    logger.info(f"Диапазон дат в данных: {df['Дата операции'].min()} - {df['Дата операции'].max()}")

            return json.dumps({"error": "Нет данных за указанный период"}, ensure_ascii=False)

        # Формирование ответа
        result: Dict[str, Any] = {
            "greeting": greeting(),
            "cards": process_cards_data(filtered_df),
            "top_transactions": get_top_transactions(filtered_df),
            "currency_rates": get_currency_rates("../files/user_settings.json"),
            "stock_prices": get_stock_prices("../files/user_settings.json"),
        }

        return json.dumps(result, ensure_ascii=False, indent=2)

    except Exception as e:
        logger.error(f"Ошибка в главной функции: {e}")
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    # Тестовый вызов
    input_time = "2021-12-31 14:30:00"
    result_json = main_function(input_time)
    print(result_json)
