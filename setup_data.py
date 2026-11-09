"""Télécharge les matchs ATP/WTA, les importe, puis calcule les notes Elo.
Peut être lancé en ligne de commande ou depuis le site (/setup)."""
import urllib.request
from pathlib import Path

from db import SessionLocal, init_db
from sackmann import import_year
from elo import run_db

ANNEES = range(2015, 2026)
REPOS = {"atp": "tennis_atp", "wta": "tennis_wta"}


def telecharger(tour, annee, log):
    dest = Path("data") / f"{tour}_matches_{annee}.csv"
    dest.parent.mkdir(exist_ok=True)
    if not dest.exists():
        url = (f"https://raw.githubusercontent.com/JeffSackmann/"
               f"{REPOS[tour]}/master/{tour}_matches_{annee}.csv")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            log(f"{tour} {annee} introuvable ({e})")
            return None
    return dest


def tout_faire(log=print):
    init_db()
    with SessionLocal() as s:
        for tour in REPOS:
            for a in ANNEES:
                p = telecharger(tour, a, log)
                if p:
                    log(f"{tour} {a} : {import_year(s, tour, p)} matchs importes")
    for tour in REPOS:
        log("Calcul des notes " + tour + "...")
        log(run_db(tour))
    log("TERMINE")


if __name__ == "__main__":
    tout_faire()
