from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    likes = relationship(
        'Like', back_populates='user', cascade='all, delete-orphan')
    ratings = relationship(
        'Rating', back_populates='user', cascade='all, delete-orphan')
