from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=100)


class PromptResponse(BaseModel):
    ai_response: str = Field(...)
