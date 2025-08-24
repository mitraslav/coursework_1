import pytest
from src.services import find_person_transfers

def test_find_person_transfers(sample_operations):
    result = find_person_transfers(sample_operations)
    assert len(result) == 4
    descriptions = [op["Описание"] for op in result]
    assert "Валерий А." in descriptions
    assert "Сергей З." in descriptions
    assert "Артем П." in descriptions
    assert "Иван С." in descriptions
    assert "ООО Рога и копыта" not in descriptions