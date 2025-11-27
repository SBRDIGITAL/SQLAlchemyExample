"""Абстрактный пример использования SQLAlchemy, DAO и Pydantic-схем.

Запускать из корня:
python main.py


Перед запуском скопируйте `.env.template` в `.env` и заполните
параметры подключения к тестовой БД.
"""

from asyncio import run

from app.config.config_reader import env_config
from app.database.models import metadata_obj
from app.database.connection import db_connection

from app.dao.user import user_dao
from app.dao.product import product_dao
from app.dao.order import order_dao

from app.schemas.user import NewUser
from app.schemas.order import NewOrder
from app.schemas.product import NewProduct



async def main() -> None:
    """
    ## Минимальный сценарий работы с DAO и моделями.

    Демонстрирует полный цикл работы:
    1. Читаем конфиг из `.env` через `env_config`.
    2. Создаём таблицы по `metadata_obj`.
    3. Через DAO создаём пользователя, товар и заказ.
    4. Читаем заказы пользователя обратно из БД.
    
    Returns:
        None: Выводит результаты операций в консоль.
    """

    print(f"Подключаемся к БД: {env_config.DATABASE_URL_asyncpg}")

    # Создаём таблицы для примера
    async with db_connection.get_session() as session:
        conn = await session.connection()
        await conn.run_sync(metadata_obj.create_all)

    async with db_connection.get_session() as session:
        # 1. Пользователь
        new_user = NewUser(email='user@example.com', full_name='Example User')
        user = await user_dao.create(new_user, session=session)

        # 2. Товар
        new_product = NewProduct(name='Test product', price=100)
        product = await product_dao.create(new_product, session=session)

        # 3. Заказ
        new_order = NewOrder(user_id=user.id, product_id=product.id, quantity=2)
        order = await order_dao.create(new_order, session=session)

        # 4. Получаем все заказы пользователя
        orders = await order_dao.get_by_user(user_id=user.id, session=session)

        print(f"Создан пользователь: {user}")
        print(f"Создан товар: {product}")
        print(f"Создан заказ: {order}")
        print(f"Все заказы пользователя: {orders}")



if __name__ == "__main__":
    run(main())