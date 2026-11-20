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
    import models  # noqa: F401
    Base.metadata.create_all(engine)
    from sqlalchemy import text
    for col, typ in (("p_sets", "FLOAT"), ("ligne_sets", "FLOAT"), ("total_sets", "INTEGER"), ("ok_sets", "INTEGER")):
        try:
            with engine.begin() as c:
                c.execute(text(f"ALTER TABLE predictions ADD COLUMN IF NOT EXISTS {col} {typ}"))
        except Exception:
            pass
