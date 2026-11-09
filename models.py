from sqlalchemy import String, Integer, Float, Date, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Player(Base):
    __tablename__ = "players"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # "atp:104925"
    tour: Mapped[str] = mapped_column(String(3))
    name: Mapped[str] = mapped_column(String)
    hand: Mapped[str | None] = mapped_column(String(1), nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    country: Mapped[str | None] = mapped_column(String(3), nullable=True)


class Tournament(Base):
    __tablename__ = "tournaments"
    id: Mapped[str] = mapped_column(String, primary_key=True)  # "atp:2024-580"
    tour: Mapped[str] = mapped_column(String(3))
    name: Mapped[str] = mapped_column(String)
    surface: Mapped[str | None] = mapped_column(String(10), nullable=True)  # Hard/Clay/Grass/Carpet
    level: Mapped[str | None] = mapped_column(String(2), nullable=True)  # G, M, A, F...
    best_of: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Match(Base):
    __tablename__ = "matches"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tour: Mapped[str] = mapped_column(String(3))
    tourney_id: Mapped[str] = mapped_column(ForeignKey("tournaments.id"))
    match_num: Mapped[int] = mapped_column(Integer)
    date: Mapped[object] = mapped_column(Date, index=True)
    surface: Mapped[str | None] = mapped_column(String(10), nullable=True)
    round: Mapped[str | None] = mapped_column(String(5), nullable=True)
    best_of: Mapped[int | None] = mapped_column(Integer, nullable=True)
    winner_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    loser_id: Mapped[str] = mapped_column(ForeignKey("players.id"))
    score: Mapped[str | None] = mapped_column(String, nullable=True)
    minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Stats de service (None si absentes : Challengers, anciennes années...)
    w_ace: Mapped[int | None] = mapped_column(Integer, nullable=True)
    w_df: Mapped[int | None] = mapped_column(Integer, nullable=True)
    w_svpt: Mapped[int | None] = mapped_column(Integer, nullable=True)
    w_1stin: Mapped[int | None] = mapped_column(Integer, nullable=True)
    w_1stwon: Mapped[int | None] = mapped_column(Integer, nullable=True)
    w_2ndwon: Mapped[int | None] = mapped_column(Integer, nullable=True)
    l_ace: Mapped[int | None] = mapped_column(Integer, nullable=True)
    l_df: Mapped[int | None] = mapped_column(Integer, nullable=True)
    l_svpt: Mapped[int | None] = mapped_column(Integer, nullable=True)
    l_1stin: Mapped[int | None] = mapped_column(Integer, nullable=True)
    l_1stwon: Mapped[int | None] = mapped_column(Integer, nullable=True)
    l_2ndwon: Mapped[int | None] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        UniqueConstraint("tourney_id", "match_num", name="uq_match"),
        Index("ix_match_tour_date", "tour", "date"),
    )


class EloRating(Base):
    """Rating de chaque joueur APRÈS un match (sert au backtest et à la prédiction)."""
    __tablename__ = "elo_ratings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    match_id: Mapped[int] = mapped_column(ForeignKey("matches.id"), index=True)
    player_id: Mapped[str] = mapped_column(ForeignKey("players.id"), index=True)
    date: Mapped[object] = mapped_column(Date)
    elo_global: Mapped[float] = mapped_column(Float)
    elo_surface: Mapped[float] = mapped_column(Float)
    surface: Mapped[str | None] = mapped_column(String(10), nullable=True)

