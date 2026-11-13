import threading
import time
from datetime import date
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import func
from db import SessionLocal, init_db
from models import EloRating, Player, Prediction

app = FastAPI(title="Pronostics Tennis")
init_db()

ETAT = {"etat": "inactif", "journal": []}


# ---------- tâche automatique ----------
# Sur Vercel, aucune boucle de fond ne peut tourner : les pronostics et les
# résultats sont mis à jour par GitHub Actions (suivi.cycle()), pas par ce site.
@app.get("/api/cron")
def cron():
    """Affiche seulement l'état du dernier tour (la mise à jour se fait via GitHub Actions)."""
    import suivi
    return {"statut": "ok", "dernier_tour": suivi.ETAT_CYCLE}


# ---------- pages ----------
@app.get("/", response_class=HTMLResponse)
def accueil():
    from page import PAGE
    return PAGE


@app.get("/health")
def health():
    return {"statut": "ok"}


@app.get("/api/calendrier")
def calendrier(tour: str = "atp", date_: str = Query(None, alias="date"), brut: int = 0):
    """Matchs du jour (ESPN) + pronostic enregistré. Ex : /api/calendrier?tour=atp&date=2026-11-10"""
    from espn import matchs_du_jour, brut as flux_brut
    try:
        jour = date.fromisoformat(date_) if date_ else date.today()
        if brut:
            return {"brut": flux_brut(tour, jour)}
        matchs = matchs_du_jour(tour, jour)
        with SessionLocal() as s:
            preds = {p.cle: p for p in s.query(Prediction).filter(
                Prediction.jour == jour, Prediction.tour == tour)}
        for m in matchs:
            p = preds.get(f"{tour}|{jour}|{m['a']}|{m['b']}")
            m["p_a"] = p.p_a if p else None
            m["surface"] = p.surface if p else None
            m["ok"] = p.ok_vainqueur if p else None
        return {"jour": str(jour), "matchs": matchs}
    except Exception as e:  # noqa: BLE001
        return {"erreur": repr(e)}


@app.get("/api/suivi")
def api_suivi():
    import suivi
    try:
        return suivi.stats()
    except Exception as e:  # noqa: BLE001
        return {"erreur": repr(e)}


@app.get("/match")
def match(tour: str, a: str, b: str, surface: str = "auto", best_of: int = 0,
          ligne: float | None = None, tournoi: str | None = None):
    """Ex : /match?tour=atp&a=Sinner&b=Alcaraz&tournoi=Paris Masters (surface et format automatiques)"""
    from predict import pronostic
    return pronostic(tour, a, b, surface, best_of, ligne, tournoi)


# ---------- import initial des matchs historiques ----------
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
    """Lance l'import des matchs + le calcul Elo en arrière-plan.
    (Sur Vercel, préférer le lancer via GitHub Actions : voir le workflow.)"""
    if ETAT["etat"] == "en cours":
        return {"message": "deja en cours, ouvre /setup/status"}
    ETAT["etat"], ETAT["journal"] = "en cours", []
    threading.Thread(target=_travail, daemon=True).start()
    return {"message": "lance, ouvre /setup/status pour suivre"}


@app.get("/setup/status")
def setup_status():
    return ETAT


@app.get("/top/{tour}")
def top(tour: str, n: int = 20, jours: int = 365):
    """Les n joueurs les mieux notés, actifs sur les `jours` derniers jours (tour = atp ou wta)."""
    from datetime import timedelta
    with SessionLocal() as s:
        derniere = (s.query(func.max(EloRating.date))
                    .join(Player, Player.id == EloRating.player_id)
                    .filter(Player.tour == tour).scalar())
        if derniere is None:
            return []
        limite = derniere - timedelta(days=jours)
        derniers = (s.query(func.max(EloRating.id))
                    .join(Player, Player.id == EloRating.player_id)
                    .filter(Player.tour == tour)
                    .group_by(EloRating.player_id).subquery())
        rows = (s.query(Player.name, EloRating.elo_global, EloRating.date)
                .join(Player, Player.id == EloRating.player_id)
                .filter(EloRating.id.in_(derniers), EloRating.date >= limite)
                .order_by(EloRating.elo_global.desc()).limit(n).all())
        return [{"joueur": r[0], "note": round(r[1]), "dernier_match": str(r[2])}
                for r in rows]
import glob
from fastapi.responses import FileResponse, JSONResponse


def _fichier_icone():
    trouves = glob.glob("t*chargement*.png")
    return trouves[0] if trouves else None


@app.get("/icone-512.png", include_in_schema=False)
def icone_512():
    f = _fichier_icone()
    if not f:
        return JSONResponse({"erreur": "icone introuvable"}, status_code=404)
    return FileResponse(f)


@app.get("/manifest.json", include_in_schema=False)
def manifest():
    return JSONResponse({
        "name": "Pronostics Tennis", "short_name": "Tennis",
        "start_url": "/", "display": "standalone",
        "background_color": "#0b1220", "theme_color": "#0b1220",
        "icons": [{"src": "/icone-512.png", "sizes": "512x512", "type": "image/png"}]})
