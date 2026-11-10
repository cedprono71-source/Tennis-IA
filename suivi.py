"""Suivi automatique : enregistre les pronostics AVANT les matchs, puis les compare aux résultats."""
import threading
from datetime import datetime, timedelta
from math import log

from db import SessionLocal
from models import Prediction
import espn
import predict

_VERROU = threading.Lock()
ETAT_CYCLE = {"dernier": None, "resume": "jamais lance"}
MOTS_ANNULES = ("retire", "walkover", "cancel", "abandon", "default", "suspend", "postpon")


def aujourdhui():
    return datetime.now(espn.TZ).date()


def cle(tour, jour, a, b):
    return f"{tour}|{jour}|{a}|{b}"


def calculer(m):
    out = predict.pronostic(m["tour"], m["a"], m["b"], "auto", 0, None, m["tournoi"])
    if "erreur" in out:
        return None
    esp = out["jeux_attendus"]
    ligne = int(esp) + 0.5
    return {
        "surface": out["surface"],
        "best_of": 5 if "5" in out.get("format", "") else 3,
        "p_a": list(out["proba_victoire_elo"].values())[0],
        "jeux_attendus": esp,
        "ligne": ligne,
        "p_over": out["over"].get(str(ligne)),
    }


def creer_pronostics(max_nouveaux=25):
    n, today = 0, aujourdhui()
    with SessionLocal() as s:
        for d in range(0, 3):
            jour = today + timedelta(days=d)
            for tour in ("atp", "wta"):
                try:
                    matchs = espn.matchs_du_jour(tour, jour)
                except Exception:
                    continue
                for m in matchs:
                    if m["etat"] == "post":
                        continue
                    k = cle(tour, jour, m["a"], m["b"])
                    if s.query(Prediction.id).filter_by(cle=k).first():
                        continue
                    if n >= max_nouveaux:
                        return n
                    try:
                        c = calculer(m)
                    except Exception:
                        c = None
                    base = dict(cle=k, tour=tour, jour=jour, tournoi=m["tournoi"], a=m["a"], b=m["b"])
                    s.add(Prediction(**base, **c) if c else Prediction(**base, statut="annule"))
                    s.commit()
                    n += 1
    return n


def maj_resultats():
    today, fait = aujourdhui(), 0
    with SessionLocal() as s:
        attente = s.query(Prediction).filter(Prediction.statut == "attente",
                                             Prediction.jour <= today).all()
        groupes = {}
        for p in attente:
            groupes.setdefault((p.tour, p.jour), []).append(p)
        for (tour, jour), lst in groupes.items():
            try:
                idx = {cle(tour, jour, m["a"], m["b"]): m for m in espn.matchs_du_jour(tour, jour)}
            except Exception:
                continue
            for p in lst:
                m = idx.get(p.cle)
                vieux = (today - jour).days > 3
                if not m or m["etat"] != "post":
                    if vieux:
                        p.statut = "annule"
                    continue
                st = (m["statut"] or "").lower()
                if m["gagnant"] is None or any(x in st for x in MOTS_ANNULES):
                    p.statut = "annule"
                    continue
                total = sum(sum(x) for x in m["scores"])
                p.gagnant, p.total_jeux, p.statut = m["gagnant"], total, "fait"
                p.ok_vainqueur = int((p.p_a > 0.5) == (m["gagnant"] == 0))
                if p.ligne is not None and p.p_over is not None and total > 0:
                    p.ok_over = int((p.p_over > 0.5) == (total > p.ligne))
                fait += 1
            s.commit()
    return fait


def cycle():
    """Un tour complet : nouveaux pronostics + résultats. Un seul à la fois."""
    if not _VERROU.acquire(blocking=False):
        return "deja en cours"
    try:
        r = maj_resultats()
        n = creer_pronostics()
        ETAT_CYCLE["dernier"] = datetime.now(espn.TZ).strftime("%d/%m %H:%M")
        ETAT_CYCLE["resume"] = f"{n} nouveaux pronostics, {r} resultats enregistres"
    except Exception as e:  # noqa: BLE001
        ETAT_CYCLE["resume"] = f"erreur : {e!r}"
    finally:
        _VERROU.release()
    return ETAT_CYCLE["resume"]


def calc_stats(rows):
    """rows : pronostics terminés (statut 'fait'). Fonction pure."""
    def moy(l):
        return sum(l) / len(l) if l else None

    def r(x, k=4):
        return None if x is None else round(x, k)

    y = [1.0 if p.gagnant == 0 else 0.0 for p in rows]
    ps = [min(max(p.p_a, 1e-6), 1 - 1e-6) for p in rows]
    forts = [p for p in rows if max(p.p_a, 1 - p.p_a) >= 0.65]
    ou = [p for p in rows if p.ok_over is not None]
    par_tour = {}
    for t in ("atp", "wta"):
        L = [p for p in rows if p.tour == t]
        par_tour[t] = {"n": len(L), "reussite": r(moy([p.ok_vainqueur for p in L]))}
    return {
        "n": len(rows),
        "vainqueur": {
            "reussite": r(moy([p.ok_vainqueur for p in rows])),
            "brier": r(moy([(p - yy) ** 2 for p, yy in zip(ps, y)])),
            "log_loss": r(moy([-(log(p) if yy else log(1 - p)) for p, yy in zip(ps, y)])),
            "forts_n": len(forts),
            "forts_reussite": r(moy([p.ok_vainqueur for p in forts])),
        },
        "over_under": {
            "n": len(ou),
            "reussite": r(moy([p.ok_over for p in ou])),
            "jeux_prevus": r(moy([p.jeux_attendus for p in ou]), 2),
            "jeux_reels": r(moy([p.total_jeux for p in ou]), 2),
        },
        "par_tour": par_tour,
    }


def stats():
    with SessionLocal() as s:
        faits = s.query(Prediction).filter(Prediction.statut == "fait").all()
        attente = s.query(Prediction).filter(Prediction.statut == "attente").count()
        derniers = (s.query(Prediction).filter(Prediction.statut == "fait")
                    .order_by(Prediction.jour.desc(), Prediction.id.desc()).limit(25).all())
        out = calc_stats(faits)
        out["en_attente"] = attente
        out["cycle"] = ETAT_CYCLE
        out["derniers"] = [{
            "jour": str(p.jour), "tournoi": p.tournoi, "a": p.a, "b": p.b, "p_a": round(p.p_a, 3),
            "gagnant": p.gagnant, "total_jeux": p.total_jeux, "ligne": p.ligne,
            "p_over": None if p.p_over is None else round(p.p_over, 3),
            "ok_vainqueur": p.ok_vainqueur, "ok_over": p.ok_over,
        } for p in derniers]
        return out

