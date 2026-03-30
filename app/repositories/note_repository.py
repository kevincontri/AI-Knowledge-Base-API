from .interfaces.note_repository import NoteRepositoryInterface
from app.models.note import Note
from app.database.database import Database
from sqlalchemy import insert, select, update, delete
from typing import Optional

class NoteRepository(NoteRepositoryInterface):
    async def create_note(self, title: str, content: str, user_id: int):
        async with Database() as db:
            query = (
                insert(Note).
                values(title=title, content=content, user_id=user_id)
            )
            await db.session.execute(query)
            await db.session.commit()
            return 1
        
        return None
    
    async def get_note_by_id(self, note_id: int):
        async with Database() as db:
            query = (
                select(Note).
                where(Note.c.id == note_id)
            )
            result = await db.session.execute(query)
            row = result.fetchone()
            return dict(row._mapping)
        
        return None
    
    async def get_all_notes(self):
        async with Database() as db:
            query = (
                select(Note)
            )
            result = await db.session.execute(query)
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]
        
        return None
        
    async def update_note(self, note_id: int, title: Optional[str] = None, content: Optional[str] = None):
        values = {}
        if title is not None:
            values["title"] = title
        if content is not None:
            values["content"] = content

        async with Database() as db:
            query = (
                update(Note)
                .where(Note.c.id == note_id)
                .values(**values)
            )
            await db.session.execute(query)
            await db.session.commit()
            return await self.get_note_by_id(note_id)
        
        return None
        
    async def delete_note(self, note_id: int):
        async with Database() as db:
            query = (
                delete(Note)
                .where(Note.c.id == note_id)
            )
            await db.session.execute(query)
            await db.session.commit()
            return 1
        
        return None

        