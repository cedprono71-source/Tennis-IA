import threading
from fastapi import FastAPI
from sqlalchemy import func
from db import SessionLocal, init_db
from models import EloRating, Player

app = FastAPI(title="Pronostics Tennis")
init_db()

ETAT = {"etat": "inactif", "journal": []}


@app.get("/")
def accueil():
    return {"statut": "ok"}


def _log(msg):
    ETAT["journal"].append(msg)


def _travail():
    try:
        from setup_data import tout_faire
        tout_faire(_log)
        ETAT["etat"] = "termine"
    except Exception as e:  # noqa: BLE001
        _log(f"ERREUR : {e!r}")
        ETAT["etat"] = "erreur"


@app.get("/setup")
def setup():
    """Lance l'import des matchs + le calcul Elo en arrière-plan."""
    if ETAT["etat"] == "en cours":
        return {"message": "deja en cours, ouvre /setup/status"}
    ETAT["etat"], ETAT["journal"] = "en cours", []
    threading.Thread(target=_travail, daemon=True).start()
    return {"message": "lance, ouvre /setup/status pour suivre"}


@app.get("/setup/status")
def setup_status():
    return ETAT


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
