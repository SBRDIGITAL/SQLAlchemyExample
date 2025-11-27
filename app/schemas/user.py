"""Pydantic-схемы для работы с пользователями-примера.

Используются для передачи данных между слоями DAO/сервисов и внешним кодом.
"""

from typing import Annotated

from pydantic import BaseModel, Field



class NewUser(BaseModel):
    """
    ## Модель для создания нового пользователя.

    Attributes:
        email (str): Email пользователя (уникальный, обязателен).
        full_name (str): Полное имя пользователя (для отображения).
    """
    email: Annotated[str, Field(max_length=255, description='Email пользователя')]
    full_name: Annotated[str, Field(max_length=255, description='Полное имя пользователя')]


class ExistsUser(NewUser):
    """
    ## Модель существующего пользователя (как хранится в БД).

    Наследует поля из :class:`NewUser` и добавляет первичный ключ.
    
    Attributes:
        id (int): Первичный ключ пользователя в таблице.
    """
    id: int


# Публичный API модуля
__all__ = ['NewUser', 'ExistsUser']