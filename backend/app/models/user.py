
from datetime import datetime
from typing import Optional
import uuid

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    cv_text: Optional[str] = None  # stored for AI context
    created_at: datetime = Field(default_factory=datetime.utcnow)