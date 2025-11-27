"""Минимальный конфиг для примера SQLAlchemyExample.

Показывает, как в проекте читается `.env` через Pydantic Settings.
"""

from os.path import join

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict



class DotEnvConfig(BaseSettings):
	"""
	## Конфигурация для примера работы с SQLAlchemy.

	Используется только небольшое подмножество настроек из основного проекта:
	строка подключения к базе данных и флаг логирования запросов.

	### Attributes:
		DATABASE_URL_asyncpg (str): URL подключения к БД в формате `postgresql+asyncpg://...`.
		DB_ECHO (bool): Включение/выключение логов SQLAlchemy.
	"""

	# Минимально необходимый набор для примера
	POSTGRES_DB: SecretStr
	POSTGRES_USER: SecretStr
	POSTGRES_PASSWORD: SecretStr
	POSTGRES_HOST: SecretStr
	POSTGRES_PORT: SecretStr

	DB_ECHO: bool = False

	@property
	def DATABASE_URL_asyncpg(self) -> str:
		"""
		## Строка подключения к базе данных `PostgreSQL`.
		
		Returns:
			str: URL в формате `postgresql+asyncpg://user:password@host:port/db`.
		"""
		return (
			f"postgresql+asyncpg://{self.POSTGRES_USER.get_secret_value()}"
			f":{self.POSTGRES_PASSWORD.get_secret_value()}"
			f"@{self.POSTGRES_HOST.get_secret_value()}"
			f":{self.POSTGRES_PORT.get_secret_value()}"
			f"/{self.POSTGRES_DB.get_secret_value()}"
		)

	model_config = SettingsConfigDict(
		env_file=join('.env'),
		env_file_encoding='utf-8',
	)


# Создание экземпляра конфигурации
env_config = DotEnvConfig()

# Публичный API модуля
__all__ = ['DotEnvConfig', 'env_config']