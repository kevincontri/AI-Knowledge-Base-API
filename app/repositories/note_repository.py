from .interfaces.note_repository import NoteRepositoryInterface
from app.models.note import Note
from app.database.database import Database
from sqlalchemy import insert, select, update, delete
from typing import Optional


class NoteRepository(NoteRepositoryInterface):
    async def create_note(self, title: str, content: str, user_id: int):
        async with Database() as db:
            query = (
                insert(Note)
                .values(title=title, content=content, user_id=user_id)
                .returning(Note)
            )
            result = await db.session.execute(query)
            await db.session.commit()

            inserted_note = result.fetchone()
            return dict(inserted_note._mapping)

        return False

    async def get_note_from_user(self, note_id: int, user_id: int):
        async with Database() as db:
            query = select(Note).where(Note.c.id == note_id, Note.c.user_id == user_id)
            result = await db.session.execute(query)
            note = result.one_or_none()
            if note:
                return dict(note._mapping)
            return None

        return None

    async def get_all_notes_from_user(self, user_id: int):
        async with Database() as db:
            query = select(Note).where(Note.c.user_id == user_id)
            result = await db.session.execute(query)
            rows = result.fetchall()

            return [dict(row._mapping) for row in rows] if rows else None

        return None

    async def update_note_from_user(
        self,
        note_id: int,
        user_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
    ):
        if not await self.__verify_user_note(note_id, user_id):
            return None
        else:
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
                    .returning(Note)
                )
                result = await db.session.execute(query)
                await db.session.commit()
                updated_note = result.fetchone()
                return dict(updated_note._mapping)

        return None

    async def delete_note_from_user(self, note_id: int, user_id: int):
        if not await self.__verify_user_note(note_id, user_id):
            return None

        async with Database() as db:
            query = delete(Note).where(Note.c.id == note_id)
            await db.session.execute(query)
            await db.session.commit()
            return True

        return None

    async def get_user_notes(self, user_id: int):
        async with Database() as db:
            query = select(Note).where(Note.c.user_id == user_id)
            result = await db.session.execute(query)
            rows = result.fetchall()
            return [dict(row._mapping) for row in rows]

    async def __verify_user_note(self, note_id: int, user_id: int):
        note = await self.get_note_from_user(note_id, user_id)
        if not note:
            return False
        return int(note.get("user_id")) == int(user_id)
