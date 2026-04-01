from fastapi import FastAPI
from .user_controller import user_router
from .note_controller import note_router

app = FastAPI()

app.include_router(user_router)
app.include_router(note_router)