from fastapi import APIRouter, HTTPException, Depends, Path
from app.schemas.note_schemas import *
from app.controllers.dependencies import *
from app.exceptions.exceptions import *
from app.core.auth import get_current_user

note_router = APIRouter(prefix="/notes", tags=["notes"])


@note_router.post("", status_code=201)
async def create_note(
    body: NoteCreate,
    note_service: NoteService = Depends(get_note_service),
    current_user_id=Depends(get_current_user),
):
    try:
        note = await note_service.create_note(body.title, body.content, current_user_id)
        return SingleNoteResponse(note=note)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@note_router.get("", status_code=200)
async def get_all_notes_from_user(
    note_service: NoteService = Depends(get_note_service),
    current_user_id=Depends(get_current_user),
):
    notes = await note_service.get_all_notes_from_user(current_user_id)
    return MultipleNoteResponse(count=len(notes), notes=notes)


@note_router.get("/{note_id}", status_code=200, response_model=SingleNoteResponse)
async def get_note_from_user(
    note_id: int = Path(..., gt=0),
    note_service: NoteService = Depends(get_note_service),
    current_user_id=Depends(get_current_user),
):
    try:
        note = await note_service.get_note_from_user(note_id, current_user_id)
        return SingleNoteResponse(note=note)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@note_router.put("/{note_id}", status_code=200)
async def update_note_from_user(
    body: NoteUpdate,
    note_id: int = Path(..., gt=0),
    note_service: NoteService = Depends(get_note_service),
    current_user_id=Depends(get_current_user),
):

    if body.title is None and body.content is None:
        raise HTTPException(
            status_code=400, detail="At least one field must be provided"
        )
    try:
        note_updated = await note_service.update_note_from_user(
            note_id, current_user_id, body.title, body.content
        )
        return SingleNoteResponse(note=note_updated)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@note_router.delete("/{note_id}", status_code=204)
async def delete_from_user(
    note_id: int = Path(..., gt=0),
    note_service: NoteService = Depends(get_note_service),
    current_user_id=Depends(get_current_user),
):
    try:
        await note_service.delete_note_from_user(note_id, current_user_id)
        return
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
