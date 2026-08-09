"""
FinAI Pro
Database Configuration

Creates the SQLite database connection,
database session, and base model class.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    """
    Provides a database session to FastAPI routes.
    """

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()