from pydantic import BaseModel, Field
from typing import List


class UserCreate(BaseModel):
    username: str = Field(..., max_length=100, min_length=3)
    password: str = Field(..., min_length=8, max_length=30)


class User(BaseModel):
    id: int
    username: str
    created_at: str


class SingleUserResponse(BaseModel):
    user: User


class MultipleUserResponse(BaseModel):
    count: int
    users: List[User]


class UserLogin(BaseModel):
    username: str = Field(..., max_length=100, min_length=3)
    password: str = Field(..., min_length=8, max_length=30)
