from pydantic import BaseModel
from typing import Optional


class BlogCreate(BaseModel):
    title: str
    text: str
    is_published: Optional[bool] = True


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    is_published: Optional[bool] = None


class BlogDelete(BaseModel):
    title: Optional[str] = ''
    text: Optional[str] = ''
    is_published: Optional[bool] = True


class BlogResponse(BaseModel):
    title: str
    text: str
    is_published: bool

    class Config:
        orm_mode = True
