from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from models.blog import Blog
from models.user import User


DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создание таблиц на основе импортированных моделей
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
