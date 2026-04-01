from fastapi import APIRouter, HTTPException, Depends
from app.schemas.note_schemas import *
from fastapi.responses import JSONResponse
from app.controllers.json_output import *
from app.controllers.dependencies import *

note_router = APIRouter(
    prefix="/notes",
    tags=["notes"],
)

@note_router.post("/")
async def create_note(body: NoteCreate, note_service: NoteService = Depends(get_note_service)):
    try:
        note_created = await note_service.create_note(body.title, body.content, body.user_id)
        if note_created:
            return JSONResponse(
                content={"message": "Note created successfully"}, 
                status_code=201
                )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
            )

@note_router.get("/")
async def get_all_notes(note_service: NoteService = Depends(get_note_service)):
    notes = await note_service.get_all_notes()
    notes_formatted = format_multiple_notes(notes)
    return JSONResponse(
        content=notes_formatted, 
        status_code=200
        )

@note_router.get("/{note_id}")
async def get_note_by_id(note_id: int, note_service: NoteService = Depends(get_note_service)):
    try:
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
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
            )

@note_router.put("/{note_id}")
async def update_note(body: NoteUpdate, note_id: int, note_service: NoteService = Depends(get_note_service)):
    try:
        note_updated = await note_service.update_note(note_id, body.title, body.content)
        if note_updated:
            note_updated_formatted = format_single_note(note_updated)
            return JSONResponse(
                content={"note updated": note_updated_formatted}, 
                status_code=200
                )
            
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
            )

@note_router.delete("/{note_id}")
async def delete_note(note_id: int, note_service: NoteService = Depends(get_note_service)):
    try:
        note_deleted = await note_service.delete_note(note_id)
        if note_deleted:
            return JSONResponse(
                content={"message": "Note deleted successfully"}, 
                status_code=200
                )
    except Exception as e:
        raise HTTPException(
            status_code=400, 
            detail=str(e)
        )
