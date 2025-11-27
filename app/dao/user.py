"""DAO-слой для работы с пользователями-примера (`User`)."""

from typing import Optional
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO

from app.database.models import User
from app.schemas.user import NewUser, ExistsUser



class UserDAO(BaseDAO):
    """
    ## DAO для работы с пользователями-примера (`User`).
    
    Attributes:
        model: Класс модели SQLAlchemy для пользователя (`User`).
    """
    def __init__(self) -> None:
        """
        ## Инициализирует `UserDAO`.

        Устанавливает модель `User` для работы с пользователями.
        """
        super().__init__()
        self.model = User

    async def create(self, user: NewUser, session: AsyncSession) -> ExistsUser:
        """
        ## Создаёт пользователя.

        Args:
            user: Pydantic-модель с данными пользователя.
            session: Асинхронная сессия БД.

        Returns:
            ExistsUser: Созданный пользователь с заполненным `id`.
        """
        stmt = (
            insert(self.model)
            .values(**user.model_dump())
            .returning(self.model)
        )
        res = await session.execute(stmt)
        await session.flush()
        obj = res.scalar_one()
        return ExistsUser(**self._return_dict_from_obj(obj, self.model))

    async def get_by_email(self,
        email: str,
        session: AsyncSession
    ) -> Optional[ExistsUser]:
        """
        ## Возвращает пользователя по email или None.

        Args:
            email: Email пользователя для поиска.
            session: Асинхронная сессия БД.

        Returns:
            ExistsUser | None: Найденный пользователь или `None`, если не найден.
        """
        query = select(self.model).where(self.model.email == email)
        obj = await self._fetch_one(session, query)
        if not obj:
            return None
        return ExistsUser(**self._return_dict_from_obj(obj, self.model))

    async def hide(self, user_id: int, session: AsyncSession) -> bool:
        """
        ## Скрывает пользователя (мягкое удаление).

        Args:
            user_id: ID пользователя.
            session: Асинхронная сессия БД.

        Returns:
            bool: True, если пользователь найден и скрыт, False иначе.
        """
        query = select(self.model).where(self.model.id == user_id)
        obj = await self._fetch_one(session, query)
        if not obj:
            return False
        obj.is_hidden = True
        await session.flush()
        return True

    async def unhide(self, user_id: int, session: AsyncSession) -> bool:
        """
        ## Восстанавливает скрытого пользователя.

        Args:
            user_id: ID пользователя.
            session: Асинхронная сессия БД.

        Returns:
            bool: True, если пользователь найден и восстановлен, False иначе.
        """
        query = select(self.model).where(self.model.id == user_id)
        obj = await self._fetch_one(session, query)
        if not obj:
            return False
        obj.is_hidden = False
        await session.flush()
        return True


# Создание экземпляра DAO для пользователей
user_dao = UserDAO()

# Публичный API модуля
__all__ = ['UserDAO', 'user_dao']