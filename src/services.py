import re
import json
import logging
from typing import List, Dict, Any

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_person_transfers(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Фильтрует операции, относящиеся к переводам физическим лицам.

    Условия:
    - Категория: "Переводы"
    - В описании есть имя и первая буква фамилии с точкой (например, "Валерий А.")

    :param operations: Список операций (словарей)
    :return: Список операций, удовлетворяющих условиям
    """
    pattern = re.compile(r'^[А-Яа-я]+\s[А-Я]\.$')

    def is_person_transfer(op: Dict[str, Any]) -> bool:
        category = op.get('Категория')
        description = op.get('Описание', '')
        return category == 'Переводы' and pattern.match(description.strip()) is not None

    filtered_ops = list(filter(is_person_transfer, operations))
    logger.info(f"Found {len(filtered_ops)} person transfers")
    return filtered_ops


def get_person_transfers_json(operations: List[Dict[str, Any]]) -> str:
    """
    Возвращает JSON с транзакциями-переводами физлицам.

    :param operations: Список операций (словарей)
    :return: JSON-строка с результатами
    """
    transfers = find_person_transfers(operations)
    return json.dumps(transfers, ensure_ascii=False, indent=2)