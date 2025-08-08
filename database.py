from sqlmodel import SQLModel, create_engine, Session
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./nutrition_data.db")
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    """Create database and all tables"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session"""
    return Session(engine)
