"""
Базовый DAO для примера SQLAlchemyExample.

Повторяет ключевые идеи основного `BaseDAO` из проекта.
"""

from typing import Any, Optional, Type, TypeVar, Iterable

from pydantic import BaseModel

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Base
from app.database.connection import db_connection



# Тип переменной для моделей SQLAlchemy
TModel = TypeVar('TModel', bound=Base)
# Тип переменной для Pydantic схем
TSchema = TypeVar('TSchema', bound=BaseModel)



class BaseDAO:
    """
    ## Базовый класс DAO для примера.

    Хранит ссылку на соединение с БД и предоставляет хелперы
    для выполнения типичных запросов (`select`, преобразование в dict и т.д.).
    """
    def __init__(self) -> None:
        """
        ## Инициализирует экземпляр `BaseDAO`.

        Attributes:
            db: Объект подключения к базе данных.
        """
        self.db = db_connection

    def _return_dict_from_obj(self, obj: Any, model: type[Base]) -> dict:
        """
        ## Преобразует ORM-объект в словарь по колонкам модели.

        Args:
            obj: ORM-объект, полученный из базы данных.
            model: Класс модели SQLAlchemy, по которому берутся колонки.

        Raises:
            ValueError: Если не передан `obj` или `model`.

        Returns:
            dict: Словарь вида `{"column": value, ...}`.
        """
        if obj is None:
            raise ValueError('obj is required')
        if model is None:
            raise ValueError('model is required')

        columns = model.__table__.columns.keys()
        return {col: getattr(obj, col) for col in columns}

    def _base_select(self, model: type[TModel]) -> Select:
        """
        ## Базовый `select(model)` (короче запись).

        Args:
            model: Класс модели SQLAlchemy.

        Returns:
            Select: Объект SQLAlchemy `select` для указанной модели.
        """
        return select(model)

    @staticmethod
    def _as_schema(
        obj: Optional[Any],
        model_cls: type[Base],
        schema_cls: Type[TSchema]
    ) -> Optional[TSchema]:
        """
        ## Конвертация ORM-объекта в Pydantic-схему или None.

        Args:
            obj: ORM-объект или `None`.
            model_cls: Класс ORM-модели.
            schema_cls: Класс Pydantic-схемы для результата.

        Returns:
            TSchema | None: Экземпляр Pydantic-схемы или `None`, если `obj` пустой.
        """
        if not obj:
            return None
        base = BaseDAO()
        data = base._return_dict_from_obj(obj, model_cls)
        return schema_cls(**data)

    async def _fetch_one(self, session: AsyncSession, query: Select):
        """
        ## Выполняет запрос и возвращает один объект или None.

        Args:
            session: Асинхронная сессия БД.
            query: Объект запроса SQLAlchemy `Select`.

        Returns:
            Any | None: Один ORM-объект или `None`, если не найдено.
        """
        res = await session.execute(query)
        return res.scalar_one_or_none()

    async def _fetch_all(self, session: AsyncSession, query: Select) -> Iterable[Any]:
        """
        ## Выполняет запрос и возвращает список ORM-объектов.

        Args:
            session: Асинхронная сессия БД.
            query: Объект запроса SQLAlchemy `Select`.

        Returns:
            Iterable[Any]: Последовательность ORM-объектов.
        """
        res = await session.execute(query)
        return res.scalars().all()


# Публичный API модуля
__all__ = ['BaseDAO', 'TModel', 'TSchema']