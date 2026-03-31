from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database.base import metadata

Note = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String),
    Column("content", String),
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("created_at", DateTime, default=datetime.utcnow),
)
