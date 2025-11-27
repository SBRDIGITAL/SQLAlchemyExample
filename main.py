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

from app.modules.logging import get_logger, setup_logging



# Инициализация логирования
setup_logging()
logger = get_logger(__name__)



async def main() -> None:
    """
    ## Расширенный сценарий работы с DAO и моделями.

    Демонстрирует полный цикл работы:
    1. Читаем конфиг из `.env` через `env_config`.
    2. Создаём таблицы по `metadata_obj`.
    3. Демонстрируем все методы DAO:
       - UserDAO: create, get_by_email
       - ProductDAO: create, get_all
       - OrderDAO: create, get_by_user
    
    Returns:
        None: Выводит результаты операций в консоль.
    """

    logger.info("="*70)
    logger.info("Запуск примера SQLAlchemy + DAO")
    logger.info("="*70)
    logger.info(f"Подключаемся к БД: {env_config.DATABASE_URL_asyncpg}")

    # Создаём таблицы для примера
    async with db_connection.get_session() as session:
        conn = await session.connection()
        await conn.run_sync(metadata_obj.create_all)
        logger.info("✓ Таблицы созданы")

    async with db_connection.get_session() as session:
        logger.info("="*70)
        logger.info("ДЕМОНСТРАЦИЯ UserDAO")
        logger.info("="*70)

        # 1. Создание пользователей
        logger.info("1. Создание пользователей...")
        user1 = await user_dao.create(
            NewUser(email='alice@example.com', full_name='Alice Johnson'),
            session=session
        )
        logger.info(f"   ✓ Создан: {user1}")

        user2 = await user_dao.create(
            NewUser(email='bob@example.com', full_name='Bob Smith'),
            session=session
        )
        logger.info(f"   ✓ Создан: {user2}")

        # 2. Поиск пользователя по email
        logger.info("2. Поиск пользователя по email...")
        found_user = await user_dao.get_by_email('alice@example.com', session=session)
        logger.info(f"   ✓ Найден: {found_user}")

        not_found = await user_dao.get_by_email('nonexistent@example.com', session=session)
        logger.info(f"   ✓ Не найден: {not_found}")

        logger.info("="*70)
        logger.info("ДЕМОНСТРАЦИЯ ProductDAO")
        logger.info("="*70)

        # 3. Создание товаров
        logger.info("3. Создание товаров...")
        product1 = await product_dao.create(
            NewProduct(name='Ноутбук', price=50000),
            session=session
        )
        logger.info(f"   ✓ Создан: {product1}")

        product2 = await product_dao.create(
            NewProduct(name='Мышь', price=1500),
            session=session
        )
        logger.info(f"   ✓ Создан: {product2}")

        product3 = await product_dao.create(
            NewProduct(name='Клавиатура', price=3000),
            session=session
        )
        logger.info(f"   ✓ Создан: {product3}")

        # 4. Получение всех товаров
        logger.info("4. Получение всех товаров...")
        all_products = await product_dao.get_all(session=session)
        logger.info(f"   ✓ Всего товаров: {len(all_products)}")
        for p in all_products:
            logger.info(f"     - {p.name}: {p.price} руб.")

        logger.info("="*70)
        logger.info("ДЕМОНСТРАЦИЯ OrderDAO")
        logger.info("="*70)

        # 5. Создание заказов
        logger.info("5. Создание заказов...")
        order1 = await order_dao.create(
            NewOrder(user_id=user1.id, product_id=product1.id, quantity=1),
            session=session
        )
        logger.info(f"   ✓ Заказ #{order1.id}: {user1.full_name} -> {product1.name} x{order1.quantity}")

        order2 = await order_dao.create(
            NewOrder(user_id=user1.id, product_id=product2.id, quantity=2),
            session=session
        )
        logger.info(f"   ✓ Заказ #{order2.id}: {user1.full_name} -> {product2.name} x{order2.quantity}")

        order3 = await order_dao.create(
            NewOrder(user_id=user2.id, product_id=product3.id, quantity=1),
            session=session
        )
        logger.info(f"   ✓ Заказ #{order3.id}: {user2.full_name} -> {product3.name} x{order3.quantity}")

        # 6. Получение заказов пользователя
        logger.info("6. Получение заказов по пользователям...")
        alice_orders = await order_dao.get_by_user(user_id=user1.id, session=session)
        logger.info(f"   ✓ Заказы {user1.full_name}: {len(alice_orders)} шт.")
        for order in alice_orders:
            logger.info(f"     - Заказ #{order.id}: product_id={order.product_id}, qty={order.quantity}")

        bob_orders = await order_dao.get_by_user(user_id=user2.id, session=session)
        logger.info(f"   ✓ Заказы {user2.full_name}: {len(bob_orders)} шт.")
        for order in bob_orders:
            logger.info(f"     - Заказ #{order.id}: product_id={order.product_id}, qty={order.quantity}")

        logger.info("="*70)
        logger.info("ДЕМОНСТРАЦИЯ МЕТОДОВ HIDE/UNHIDE")
        logger.info("="*70)

        # 7. Скрытие и восстановление пользователя
        logger.info("7. Мягкое удаление пользователя (hide)...")
        hide_result = await user_dao.hide(user_id=user2.id, session=session)
        logger.info(f"   ✓ Пользователь {user2.full_name} скрыт: {hide_result}")
        
        # Проверяем статус
        hidden_user = await user_dao.get_by_email('bob@example.com', session=session)
        logger.info(f"   ✓ Статус is_hidden: {hidden_user.is_hidden if hidden_user else 'N/A'}")

        # 8. Восстановление пользователя
        logger.info("8. Восстановление пользователя (unhide)...")
        unhide_result = await user_dao.unhide(user_id=user2.id, session=session)
        logger.info(f"   ✓ Пользователь {user2.full_name} восстановлен: {unhide_result}")
        
        restored_user = await user_dao.get_by_email('bob@example.com', session=session)
        logger.info(f"   ✓ Статус is_hidden: {restored_user.is_hidden if restored_user else 'N/A'}")

        # 9. Скрытие товара
        logger.info("9. Мягкое удаление товара...")
        product_hide = await product_dao.hide(product_id=product2.id, session=session)
        logger.info(f"   ✓ Товар '{product2.name}' скрыт: {product_hide}")

        # 10. Скрытие заказа
        logger.info("10. Мягкое удаление заказа...")
        order_hide = await order_dao.hide(order_id=order1.id, session=session)
        logger.info(f"   ✓ Заказ #{order1.id} скрыт: {order_hide}")
        
        # Восстановление заказа
        order_unhide = await order_dao.unhide(order_id=order1.id, session=session)
        logger.info(f"   ✓ Заказ #{order1.id} восстановлен: {order_unhide}")

        # 11. Демонстрация: связи сохраняются после скрытия
        logger.info("11. Проверка: заказы пользователя после скрытия товара...")
        all_alice_orders = await order_dao.get_by_user(user_id=user1.id, session=session)
        logger.info(f"   ✓ Заказы Alice ({len(all_alice_orders)} шт.) сохранились, несмотря на скрытие товара")
        for order in all_alice_orders:
            logger.info(f"     - Заказ #{order.id}: product_id={order.product_id} (is_hidden={order.is_hidden})")

        # Коммитим все изменения в базу данных
        await session.commit()

        logger.info("="*70)
        logger.info("✓ Все операции выполнены успешно!")
        logger.info("✓ Каскадное удаление отключено - связи сохраняются!")
        logger.info("="*70)



if __name__ == "__main__":
    run(main())