from datetime import datetime
from typing import Generator

from sqlalchemy import DateTime, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at = DateTime(timezone=True, server_default=func.now(), nullable=False)
    updated_at = DateTime(timezone=True, server_default=func.now(), onupdate=func.now(), nullable=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
