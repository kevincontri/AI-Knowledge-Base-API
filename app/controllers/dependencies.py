from fastapi import Depends
from app.services.user_service import UserService
from app.services.note_service import NoteService
from app.repositories.user_repository import UserRepository
from app.repositories.note_repository import NoteRepository
from app.services.ai_service import AIService


def get_user_repository():
    return UserRepository()


def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


def get_note_repository():
    return NoteRepository()


def get_note_service(
    note_repo: NoteRepository = Depends(get_note_repository),
    user_service: UserService = Depends(get_user_service),
):
    return NoteService(note_repo, user_service)


def get_aiservice(
    note_repo: NoteRepository = Depends(get_note_repository),
    user_repo: UserRepository = Depends(get_user_repository),
):
    return AIService(note_repo, user_repo)
