from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.database.base import metadata

User = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String),
    Column("created_at", String, default=str(datetime.now().isoformat()))
)
