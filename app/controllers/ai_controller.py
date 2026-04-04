from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ai_schemas import *
from app.controllers.dependencies import *
from app.exceptions.exceptions import NotFoundError
from app.core.auth import get_current_user

ai_router = APIRouter(prefix="/ai", tags=["ai"])


@ai_router.post("/ask", status_code=200)
async def ask(
    body: AskRequest,
    ai_service: AIService = Depends(get_aiservice),
    current_user_id=Depends(get_current_user),
):
    try:
        llm_response = await ai_service.ask(current_user_id, body.prompt)
        return llm_response

    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
