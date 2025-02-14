import os
import sys
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем путь к `src/`, чтобы Alembic видел модели
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

# Импортируем модели и базу
from src.models.base import Base
from src.models.user import User
from src.models.blog import Blog

# Проверяем, загружены ли таблицы
print("✅ Base.metadata.tables в env.py:", Base.metadata.tables)

# Указываем метаданные для Alembic
target_metadata = Base.metadata  # <=== ДОЛЖНО БЫТЬ ОБЯЗАТЕЛЬНО!

# Загружаем URL базы данных
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL не найден в переменных окружения!")

# Настройки Alembic
config = context.config
fileConfig(config.config_file_name)

# Функции для миграций
def run_migrations_offline():
    context.configure(url=DATABASE_URL, target_metadata=target_metadata, literal_binds=True, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, compare_type=True)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
