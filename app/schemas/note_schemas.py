from pydantic import BaseModel, Field

class NoteCreate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str = Field(..., max_length=1000)
    user_id: int = Field(..., gt=0)
    
class NoteUpdate(BaseModel):
    title: str = Field(None, max_length=100)
    content: str = Field(None, max_length=1000)
