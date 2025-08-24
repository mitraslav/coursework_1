import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_empty():
    """Тест с пустым датафреймом."""
    empty_df = pd.DataFrame(columns=["date", "category", "amount"])
    result = spending_by_category(empty_df, "Food")
    assert result.empty


def test_spending_by_category_nonexistent(sample_transactions):
    """Тест с несуществующей категорией."""
    result = spending_by_category(sample_transactions, "Nonexistent", "2024-04-01")
    assert result.empty
