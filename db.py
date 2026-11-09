import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Local : SQLite. En ligne : définir DATABASE_URL (Neon / Postgres).
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tennis.db")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    from app import models  # noqa: F401
    Base.metadata.create_all(engine)

