# tests/test_database.py

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from src.adapters.database import DATABASE_URL, Base, SessionLocal, engine, get_db


class TestDatabase:
    """Тесты для модуля database"""

    def test_database_url(self):
        """Тест корректности URL базы данных"""
        assert DATABASE_URL == "sqlite:///./test.db"

    def test_engine_creation(self):
        """Тест создания engine"""
        assert engine is not None
        assert str(engine.url) == DATABASE_URL

    def test_session_local(self):
        """Тест создания sessionmaker"""
        assert SessionLocal is not None
        assert callable(SessionLocal)  # Проверяем что это callable

    def test_base_declarative(self):
        """Тест базового класса для моделей"""
        assert Base is not None
        assert hasattr(Base, "metadata")

    def test_engine_connectivity(self):
        """Тест подключения к базе данных"""
        # Пытаемся выполнить простой запрос
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1

    def test_session_local_creates_session(self):
        """Тест что SessionLocal создает сессии"""
        session = SessionLocal()
        try:
            assert session is not None
            # Проверяем что сессия работает
            result = session.execute(text("SELECT 1"))
            assert result.scalar() == 1
        finally:
            session.close()

    def test_get_db_generator(self):
        """Тест генератора get_db"""
        # Создаем генератор
        db_gen = get_db()

        try:
            # Получаем первую сессию
            db1 = next(db_gen)
            assert db1 is not None

            # Проверяем что это действительно сессия
            result = db1.execute(text("SELECT 1"))
            assert result.scalar() == 1

        finally:
            # Завершаем генератор
            try:
                next(db_gen)
            except StopIteration:
                pass

    def test_database_is_sqlite(self):
        """Тест что используется SQLite"""
        assert "sqlite" in DATABASE_URL


class TestDatabaseIntegration:
    """Интеграционные тесты с реальной базой"""

    @pytest.fixture
    def test_engine(self):
        """Фикстура для тестовой базы"""
        test_engine = create_engine(
            "sqlite:///:memory:", connect_args={"check_same_thread": False}
        )
        Base.metadata.create_all(bind=test_engine)
        yield test_engine
        Base.metadata.drop_all(bind=test_engine)

    @pytest.fixture
    def test_session(self, test_engine):
        """Фикстура для тестовой сессии"""
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=test_engine
        )
        session = TestingSessionLocal()
        yield session
        session.close()

    def test_database_operations(self, test_session):
        """Тест операций с базой данных"""
        # Простая проверка работы с базой
        result = test_session.execute(text("SELECT 1 as test_value"))
        row = result.fetchone()
        assert row[0] == 1


def test_database_module_import():
    """Тест что модуль database корректно импортируется"""
    from src.adapters import database

    assert database.engine is not None
    assert database.SessionLocal is not None
    assert database.Base is not None
    assert database.get_db is not None


def test_get_db_context_manager():
    """Тест использования get_db как контекстного менеджера"""
    # Имитируем использование в FastAPI dependency
    db_gen = get_db()
    try:
        db = next(db_gen)
        assert db is not None
        # Проверяем базовые операции
        result = db.execute(text("SELECT 1"))
        assert result.scalar() == 1
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass


# Параметризованные тесты для разных сценариев
@pytest.mark.parametrize(
    "query,expected",
    [
        ("SELECT 1", 1),
        ("SELECT 2 + 2", 4),
        ("SELECT 'test'", "test"),
    ],
)
def test_database_queries(query, expected):
    """Параметризованный тест различных запросов"""
    with engine.connect() as conn:
        result = conn.execute(text(query))
        assert result.scalar() == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
