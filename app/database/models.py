"""SQLAlchemy-модели для абстрактного примера User / Product / Order."""

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, BigInteger, Integer, String, ForeignKey, Index, Boolean


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
        is_hidden (bool): Флаг мягкого удаления (скрытия записи).
    """

    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    is_hidden = Column(Boolean, nullable=False, default=False, index=True)

    orders = relationship('Order', back_populates='user')

    # Дополнительный индекс для поиска по имени
    __table_args__ = (
        Index('idx_user_full_name', 'full_name'),
    )


class Product(Base):
    """
    ## Пример товара, который можно заказать.

    Attributes:
        id (int): Первичный ключ.
        name (str): Название товара.
        price (int): Цена товара в условных единицах.
        is_hidden (bool): Флаг мягкого удаления (скрытия записи).
    """

    __tablename__ = 'products'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    price = Column(Integer, nullable=False, index=True)
    is_hidden = Column(Boolean, nullable=False, default=False, index=True)

    orders = relationship('Order', back_populates='product')

    # Составной индекс для фильтрации по имени и цене
    __table_args__ = (
        Index('idx_product_name_price', 'name', 'price'),
    )


class Order(Base):
    """
    ## Пример заказа пользователя.

    Attributes:
        id (int): Первичный ключ.
        user_id (int): Внешний ключ на пользователя.
        product_id (int): Внешний ключ на товар.
        quantity (int): Количество единиц товара.
        is_hidden (bool): Флаг мягкого удаления (скрытия записи).
    """

    __tablename__ = 'orders'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False, index=True)
    product_id = Column(BigInteger, ForeignKey('products.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    is_hidden = Column(Boolean, nullable=False, default=False, index=True)

    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

    # Составные индексы для оптимизации запросов
    __table_args__ = (
        Index('idx_order_user_id', 'user_id'),
        Index('idx_order_product_id', 'product_id'),
        Index('idx_order_user_product', 'user_id', 'product_id'),
    )


metadata_obj = Base.metadata

# Публичный API модуля
__all__ = ['Base', 'User', 'Product', 'Order', 'metadata_obj']