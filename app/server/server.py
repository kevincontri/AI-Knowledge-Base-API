from fastapi import FastAPI
from app.controllers.user_controller import user_router
from app.controllers.note_controller import note_router
from app.controllers.ai_controller import ai_router
app = FastAPI()

app.include_router(user_router)
app.include_router(note_router)
app.include_router(ai_router)