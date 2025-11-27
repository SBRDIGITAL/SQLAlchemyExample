"""DAO-слой для работы с товарами-примера (`Product`)."""

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO

from app.database.models import Product
from app.schemas.product import NewProduct, ExistsProduct



class ProductDAO(BaseDAO):
    """
    ## DAO для работы с товарами-примера (`Product`).
    
    Attributes:
        model: Класс модели SQLAlchemy для товара (`Product`).
    """
    def __init__(self) -> None:
        """
        ## Инициализирует `ProductDAO`.

        Устанавливает модель `Product` для работы с товарами.
        """
        super().__init__()
        self.model = Product

    async def create(self,
        product: NewProduct,
        session: AsyncSession
    ) -> ExistsProduct:
        """
        ## Создаёт новый товар.

        Args:
            product: Pydantic-модель с данными товара.
            session: Асинхронная сессия БД.

        Returns:
            ExistsProduct: Созданный товар с заполненным `id`.
        """
        stmt = (
            insert(self.model)
            .values(**product.model_dump())
            .returning(self.model)
        )
        res = await session.execute(stmt)
        obj = res.scalar_one()
        return ExistsProduct(**self._return_dict_from_obj(obj, self.model))

    async def get_all(self, session: AsyncSession) -> list[ExistsProduct]:
        """
        ## Возвращает список всех товаров.

        Args:
            session: Асинхронная сессия БД.

        Returns:
            list[ExistsProduct]: Список всех товаров в базе.
        """
        query = select(self.model)
        objs = await self._fetch_all(session, query)
        return [
            ExistsProduct(**self._return_dict_from_obj(obj, self.model))
            for obj in objs
        ]



# Создание экземпляра DAO для товаров
product_dao = ProductDAO()

# Публичный API модуля
__all__ = ['ProductDAO', 'product_dao']