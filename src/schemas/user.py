from typing import Union, Optional
from pydantic import BaseModel, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None


class UserBase(BaseModel):
    username: str


class User(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserInDB(BaseModel):
    id: Optional[int] = None
    username: str
    hashed_password: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)
