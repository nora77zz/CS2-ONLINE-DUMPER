from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
import os


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set")

engine = create_engine(DATABASE_URL)

class OffsetDump(SQLModel, table=True):
    __tablename__ = "offset_dumps"

    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(index=True)
    content: dict = Field(sa_column=Column(JSONB))
    hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
