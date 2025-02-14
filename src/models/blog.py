from sqlalchemy import (
    Column, Integer, String,
    Boolean, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from src.models.base import Base


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String, default='')
    is_published = Column(Boolean, default=False)

    likes = relationship(
        "Like", back_populates="blog", cascade="all, delete-orphan")
    ratings = relationship(
        "Rating", back_populates="blog", cascade="all, delete-orphan")


class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users_id'))
    blog_id = Column(Integer, ForeignKey('blog_id'))

    __table_args__ = (
        UniqueConstraint('user_id', 'blog_id', 'name_unique_like'))

    user = relationship("User", back_populates="likes")
    blog = relationship("Blog", back_populates="likes") 


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users_id'))
    blog_id = Column(Integer, ForeignKey('blog_id'))
    rating = Column(Integer, nullable=False)

    user = relationship("User", back_populates="ratings")
    blog = relationship("Blog", back_populates="ratings")