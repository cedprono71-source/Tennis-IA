from fastapi import FastAPI
from sqlalchemy import func
from db import SessionLocal, init_db
from models import EloRating, Player

app = FastAPI(title="Pronostics Tennis")
init_db()


@app.get("/")
def accueil():
    return {"statut": "ok"}


@app.get("/top/{tour}")
def top(tour: str, n: int = 20):
    """Les n joueurs les mieux notés (tour = atp ou wta)."""
    with SessionLocal() as s:
        derniers = (s.query(func.max(EloRating.id))
                    .join(Player, Player.id == EloRating.player_id)
                    .filter(Player.tour == tour)
                    .group_by(EloRating.player_id).subquery())
        rows = (s.query(Player.name, EloRating.elo_global, EloRating.date)
                .join(Player, Player.id == EloRating.player_id)
                .filter(EloRating.id.in_(derniers))
                .order_by(EloRating.elo_global.desc()).limit(n).all())
        return [{"joueur": r[0], "note": round(r[1]), "dernier_match": str(r[2])}
                for r in rows]

