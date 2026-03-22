import uuid
from datetime import datetime
from enum import StrEnum
from sqlmodel import SQLModel, Field

class EventType(StrEnum):
    NOTE = "note"
    PHONE_SCREEN = "phone_screen"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTION = "rejection"
    EMAIL = "email"

class ApplicationEvent(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    application_id: uuid.UUID = Field(foreign_key="application.id", index=True)
    event_type: EventType
    description: str
    occurred_at: datetime = Field(default_factory=datetime.utcnow)