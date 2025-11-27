"""SQLAlchemy-модели для абстрактного примера User / Product / Order."""

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey


class Base(DeclarativeBase):
    """
    ## Базовый класс моделей SQLAlchemy для примера.
    """


class User(Base):
    """
    ## Пример пользователя.

    Attributes:
        id (int): Первичный ключ.
        email (str): Уникальный email пользователя.
        full_name (str): Полное имя пользователя.
    """

    __tablename__ = 'users_example'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255), nullable=False)

    orders = relationship('Order', back_populates='user')


class Product(Base):
    """
    ## Пример товара, который можно заказать.

    Attributes:
        id (int): Первичный ключ.
        name (str): Название товара.
        price (int): Цена товара в условных единицах.
    """

    __tablename__ = 'products_example'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Integer, nullable=False)

    orders = relationship('Order', back_populates='product')


class Order(Base):
    """
    ## Пример заказа пользователя.

    Attributes:
        id (int): Первичный ключ.
        user_id (int): Внешний ключ на пользователя.
        product_id (int): Внешний ключ на товар.
        quantity (int): Количество единиц товара.
    """

    __tablename__ = 'orders_example'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users_example.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products_example.id', ondelete='CASCADE'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)

    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')


metadata_obj = Base.metadata

# Публичный API модуля
__all__ = ['Base', 'User', 'Product', 'Order', 'metadata_obj']