import threading
from datetime import date
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from sqlalchemy import func
from db import SessionLocal, init_db
from models import EloRating, Player, Prediction
import cotes as cotes_fr

app = FastAPI(title="Pronostics Tennis")
init_db()

ETAT = {"etat": "inactif", "journal": []}


# ---------- pages ----------
@app.get("/", response_class=HTMLResponse)
def accueil():
    from page import PAGE
    return PAGE


@app.get("/health")
def health():
    return {"statut": "ok"}


_PAYS = {}


def _pays(tour, nom):
    k = (tour, nom)
    if k not in _PAYS:
        with SessionLocal() as s:
            r = s.query(Player.country).filter(Player.tour == tour, Player.name.ilike(f"%{nom}%")).first()
        _PAYS[k] = r[0] if r else None
    return _PAYS[k]


@app.get("/api/calendrier")
def calendrier(tour: str = "atp", date_: str = Query(None, alias="date"), brut: int = 0):
    """Matchs du jour jouables chez un bookmaker français. Ex : /api/calendrier?tour=atp&date=2026-11-10"""
    from espn import matchs_du_jour, brut as flux_brut
    try:
        jour = date.fromisoformat(date_) if date_ else date.today()
        if brut:
            return {"brut": flux_brut(tour, jour)}
        matchs = matchs_du_jour(tour, jour)
        with SessionLocal() as s:
            preds = {p.cle: p for p in s.query(Prediction).filter(
                Prediction.jour == jour, Prediction.tour == tour)}
            filtre = cotes_fr.table_remplie(s)
            liste = cotes_fr.charger(s, tour, jour) if filtre else []
        out = []
        for m in matchs:
            c = cotes_fr.chercher(liste, m["a"], m["b"]) if filtre else None
            m["fr"] = bool(c) if filtre else None  # jouable chez un bookmaker français
            p = preds.get(f"{tour}|{jour}|{m['a']}|{m['b']}")
            m["p_a"] = p.p_a if p else None
            try:
                from predict import auto_format
                m["surface"] = p.surface if p else auto_format(tour, m["tournoi"])[0]
            except Exception:  # noqa: BLE001
                m["surface"] = None
            m["pays_a"], m["pays_b"] = _pays(tour, m["a"]), _pays(tour, m["b"])
            m["opp"] = m["valeur"] = None
            if c and m["p_a"] is not None:  # opportunité : valeur calculée, cotes jamais envoyées
                va, vb = m["p_a"] * c["a"]["cote"] - 1, (1 - m["p_a"]) * c["b"]["cote"] - 1
                if max(va, vb) >= 0.05:
                    m["opp"], m["valeur"] = (0 if va >= vb else 1), round(max(va, vb), 3)
            m["ok"] = p.ok_vainqueur if p else None
            m["lignes"] = [t["ligne"] for t in c["totaux"]] if c else None
            out.append(m)
        return {"jour": str(jour), "filtre": filtre, "matchs": out}
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
          ligne: float | None = None, tournoi: str | None = None, lignes: str | None = None):
    """Ex : /match?tour=atp&a=Sinner&b=Alcaraz&tournoi=Paris Masters (surface et format automatiques)"""
    from predict import pronostic
    liste = [float(x) for x in lignes.split(",") if x] if lignes else None
    return pronostic(tour, a, b, surface, best_of, ligne, tournoi, liste)


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
