from sqlalchemy import Column, Integer, String, Boolean
from models.base import Base


class Blog(Base):
    __tablename__ = 'blog'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    text = Column(String, default='')
    is_published = Column(Boolean, default=False)
