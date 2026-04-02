from fastapi import APIRouter, Depends, HTTPException
from app.schemas.ai_schemas import *
from app.controllers.dependencies import *
from app.exceptions.exceptions import NotFoundError
from app.ai_settings.ollama_client import OllamaClient
from app.ai_settings.prompt_enhancer import PROMPT_ENHANCER

ai_router = APIRouter(
    prefix="/ask",
    tags=["AI"]
)

@ai_router.post("", status_code=200)
async def ask(body: AskRequest, ai_service: AIService = Depends(get_aiservice)):
    try:
        user_notes = await ai_service.get_user_notes(body.user_id)
        enriched_prompt = PROMPT_ENHANCER.format(notes=user_notes, user_prompt=body.prompt)
        ollama_client = OllamaClient()
        response = await ollama_client.generate(enriched_prompt)
        llm_response = response["message"]["content"]
        
        return PromptResponse(response=llm_response)
        
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