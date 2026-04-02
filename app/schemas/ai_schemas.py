from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    prompt: str = Field(..., min_length=3, max_length=100)
    
class PromptResponse(BaseModel):
    response: str = Field(...)