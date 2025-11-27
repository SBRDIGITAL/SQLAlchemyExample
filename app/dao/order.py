"""DAO-слой для работы с заказами-примера (`Order`)."""

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO

from app.database.models import Order
from app.schemas.order import NewOrder, ExistsOrder



class OrderDAO(BaseDAO):
    """
    ## DAO для работы с заказами-примера (`Order`).
    
    Attributes:
        model: Класс модели SQLAlchemy для заказа (`Order`).
    """
    def __init__(self) -> None:
        """
        ## Инициализирует `OrderDAO`.

        Устанавливает модель `Order` для работы с заказами.
        """
        super().__init__()
        self.model = Order

    async def create(self, order: NewOrder, session: AsyncSession) -> ExistsOrder:
        """
        ## Создаёт новый заказ.

        Args:
            order: Pydantic-модель с данными заказа.
            session: Асинхронная сессия БД.

        Returns:
            ExistsOrder: Созданный заказ с заполненным `id`.
        """
        stmt = (
            insert(self.model)
            .values(**order.model_dump())
            .returning(self.model)
        )
        res = await session.execute(stmt)
        obj = res.scalar_one()
        return ExistsOrder(**self._return_dict_from_obj(obj, self.model))

    async def get_by_user(self,
        user_id: int,
        session: AsyncSession
    ) -> list[ExistsOrder]:
        """
        ## Возвращает все заказы указанного пользователя.

        Args:
            user_id: Идентификатор пользователя.
            session: Асинхронная сессия БД.

        Returns:
            list[ExistsOrder]: Список заказов пользователя.
        """
        query = select(self.model).where(self.model.user_id == user_id)
        objs = await self._fetch_all(session, query)
        return [
            ExistsOrder(**self._return_dict_from_obj(obj, self.model))
            for obj in objs
        ]


# Создание экземпляра DAO для заказов
order_dao = OrderDAO()

# Публичный API модуля
__all__ = ['OrderDAO', 'order_dao']