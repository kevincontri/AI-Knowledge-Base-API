from fastapi import APIRouter, HTTPException, Depends
from app.schemas.note_schemas import *
from app.services.note_service import NoteService
from app.services.user_service import UserService
from app.repositories.note_repository import NoteRepository
from fastapi.responses import JSONResponse
from app.controllers.json_output import *
from app.repositories.interfaces.user_repository import UserRepositoryInterface

note_router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

note_service = NoteService(NoteRepository(), UserService(UserRepositoryInterface))

@note_router.post("/")
async def create_note(body: NoteCreate):
    note_created = await note_service.create_note(body.title, body.content, body.user_id)
    if note_created:
        return JSONResponse(
            content={"message": "Note created successfully"}, 
            status_code=201
            )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Note not created"
            )

@note_router.get("/")
async def get_all_notes():
    notes = await note_service.get_all_notes()
    notes_formatted = format_multiple_notes(notes)
    return JSONResponse(
        content=notes_formatted, 
        status_code=200
        )

@note_router.get("/{note_id}")
async def get_note_by_id(note_id: int):
    note = await note_service.get_note_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=404, 
            detail="Note not found"
            )
        
    note_formatted = format_single_note(note)
    return JSONResponse(
        content=note_formatted, 
        status_code=200
    )

@note_router.put("/{note_id}")
async def update_note(body: NoteUpdate, note_id: int):
    note_updated = await note_service.update_note(note_id, body.title, body.content)
    if note_updated:
        note_updated_formatted = format_single_note(note_updated)
        return JSONResponse(
            content={"message": "Note updated successfully", "note": note_updated_formatted}, 
            status_code=200
            )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Note not updated"
            )

@note_router.delete("/{note_id}")
async def delete_note(note_id: int):
    note_deleted = await note_service.delete_note(note_id)
    if note_deleted:
        return JSONResponse(
            content={"message": "Note deleted successfully"}, 
            status_code=200
            )
    else:
        raise HTTPException(
            status_code=400, 
            detail="Note not deleted"
            )

