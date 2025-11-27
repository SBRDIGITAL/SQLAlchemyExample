"""Асинхронное подключение к БД для примера SQLAlchemyExample."""

from typing import Optional
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

from app.config.config_reader import env_config



class DbConnection:
    """
    ## Класс для работы с асинхронными сессиями базы данных.

    Использует глобальный Engine (singleton) и создаёт sessionmaker для управления сессиями.
    Согласно best practices SQLAlchemy, Engine создаётся один раз на уровне модуля,
    а DbConnection может создаваться многократно, используя один и тот же Engine.
    
    Attributes:
        engine: Глобальный асинхронный движок SQLAlchemy (singleton).
        _sessionmaker: Фабрика для создания асинхронных сессий.
    """

    def __init__(self, engine: AsyncEngine) -> None:
        """
        ## Инициализирует экземпляр `DbConnection`.

        Args:
            engine: Необязательный AsyncEngine. Если не указан, используется глобальный _engine.
        """
        self.engine: AsyncEngine = engine
        self._sessionmaker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def db_close(self, engine: Optional[AsyncEngine] = None) -> None:
        """
        ## Закрывает соединение с базой данных.

        Args:
            engine: Необязательный экземпляр движка. Если не указан,
                используется движок, сохранённый в объекте.
        """
        engine = engine or self.engine
        if engine is not None:
            await engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        """
        ## Контекстный менеджер для получения асинхронной сессии.

        Yields:
            AsyncSession: Асинхронная сессия БД.

        Raises:
            RuntimeError: Если sessionmaker не инициализирован.
            Exception: Пробрасывает любые ошибки работы с сессией
                после отката транзакции.
        """
        if not self._sessionmaker:
            raise RuntimeError('Session manager not initialized')

        async with self._sessionmaker() as session:
            try:
                session = session  # type: ignore[assignment]
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

# Глобальный Engine (Singleton) - создаётся один раз при импорте модуля
_engine: AsyncEngine = create_async_engine(
    url=env_config.DATABASE_URL_asyncpg,
    echo=env_config.DB_ECHO,
)

# Глобальный экземпляр DbConnection для использования в приложении
db_connection = DbConnection(_engine)

# Публичный API модуля
__all__ = ['db_connection', 'DbConnection']