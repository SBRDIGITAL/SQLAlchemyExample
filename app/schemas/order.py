"""Pydantic-схемы для работы с заказами-примера.

Файл показывает, как в проекте описываются входные и выходные
схемы для сущности `Order` в стиле `New*` / `Exists*`.
"""

from typing import Annotated

from pydantic import BaseModel, Field


class NewOrder(BaseModel):
    """
    ## Модель для создания нового заказа.

    Attributes:
        user_id (int): Идентификатор пользователя, который оформляет заказ.
        product_id (int): Идентификатор товара, который заказывается.
        quantity (int): Количество единиц товара (по умолчанию 1).
    """
    user_id: Annotated[int, Field(ge=1, description='ID пользователя')]
    product_id: Annotated[int, Field(ge=1, description='ID товара')]
    quantity: Annotated[int, Field(ge=1, description='Количество товара в заказе')] = 1


class ExistsOrder(NewOrder):
    """
    ## Модель существующего заказа (как хранится в БД).

    Наследует поля из :class:`NewOrder` и добавляет первичный ключ.

    Attributes:
        id (int): Первичный ключ заказа в таблице.
    """
    id: int


# Публичный API модуля
__all__ = ['NewOrder', 'ExistsOrder']