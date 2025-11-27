"""Pydantic-схемы для работы с товарами-примера."""

from typing import Annotated

from pydantic import BaseModel, Field



class NewProduct(BaseModel):
    """
    ## Модель для создания нового товара.

    Attributes:
        name (str): Название товара.
        price (int): Цена товара в условных единицах (неотрицательная).
    """
    name: Annotated[str, Field(max_length=255, description='Название товара')]
    price: Annotated[int, Field(ge=0, description='Цена товара (>= 0)')]


class ExistsProduct(NewProduct):
    """
    ## Модель существующего товара.

    Attributes:
        id (int): Первичный ключ товара в таблице.
    """
    id: int


# Публичный API модуля
__all__ = ['NewProduct', 'ExistsProduct']