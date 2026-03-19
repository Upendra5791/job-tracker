

from app.config import settings
from sqlmodel import SQLModel, create_engine, Session


engine = create_engine(settings.DATABASE_URL)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        return session