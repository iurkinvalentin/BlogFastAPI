from pydantic import BaseModel, ConfigDict, constr
from typing import Optional, Annotated


class BlogCreate(BaseModel):
    title: str
    text: str
    is_published: Optional[bool] = True


class BlogUpdate(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    is_published: Optional[bool] = None


class BlogDelete(BaseModel):
    title: Optional[str] = None
    text: Optional[str] = None
    is_published: Optional[bool] = True


class BlogResponse(BaseModel):
    title: str
    text: str
    is_published: bool

    model_config = ConfigDict(from_attributes=True)


class LikeCreate(BaseModel):
    blog_id: int


class RatingCreate(BaseModel):
    blog_id: int
    rating: Annotated[int, constr(ge=1, le=5)]


class CommentCreate(BaseModel):
    blog_id: int
    text: str


class CommentResponse(BaseModel):
    id: int
    user_id: int
    blog_id: int
    text: str

    model_config = ConfigDict(from_attributes=True)

