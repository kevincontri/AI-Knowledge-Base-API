from pydantic import BaseModel, Field
from typing import List

class UserCreate(BaseModel):
    username: str = Field(..., max_length=100, min_length=3)
    
class User(BaseModel):
    id: int
    username: str
    created_at: str
    
class SingleUserResponse(BaseModel):
    user: User
    
class MultipleUserResponse(BaseModel):
    count: int
    users: List[User]
    