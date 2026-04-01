from pydantic import BaseModel, Field
from typing import List

class NoteCreate(BaseModel):
    title: str = Field(..., min_length= 3, max_length=100)
    content: str = Field(..., min_length=3, max_length=1000)
    user_id: int = Field(..., gt=0)
    
class NoteUpdate(BaseModel):
    title: str = Field(None, min_length=3, max_length=100)
    content: str = Field(None, min_length=3, max_length=1000)

class Note(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=3, max_length=1000)
    user_id: int = Field(..., gt=0)
    created_at: str

class SingleNoteResponse(BaseModel):
    note: Note
    
class MultipleNoteResponse(BaseModel):
    count: int
    notes: List[Note]
    