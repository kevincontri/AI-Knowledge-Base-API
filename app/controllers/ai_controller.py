from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ai_schemas import *
from app.controllers.dependencies import *
from app.exceptions.exceptions import NotFoundError

ai_router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@ai_router.post("/ask", status_code=200)
async def ask(body: AskRequest, ai_service: AIService = Depends(get_aiservice)):
    try:
        llm_response = await ai_service.ask(body.user_id, body.prompt)
        return llm_response
    except NotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail=str(e)
            )

    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=str(e)
            )