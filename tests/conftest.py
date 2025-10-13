# tests/conftest.py
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # корень репозитория
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from src.database import engine, Base


@pytest.fixture(autouse=True)
def clean_db():
    """Очищает базу данных перед каждым тестом"""
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    # Создаем таблицы заново
    Base.metadata.create_all(bind=engine)
    yield
    # После теста тоже очищаем
    Base.metadata.drop_all(bind=engine)
