"""Télécharge les matchs ATP/WTA, les importe, puis calcule les notes Elo.
Lancer une seule fois :  python setup_data.py
(Variable optionnelle : DATABASE_URL = adresse de ta base Neon)"""
import urllib.request
from pathlib import Path

from db import SessionLocal, init_db
from sackmann import import_year
from elo import run_db

ANNEES = range(2015, 2026)
REPOS = {"atp": "tennis_atp", "wta": "tennis_wta"}


def telecharger(tour, annee):
    dest = Path("data") / f"{tour}_matches_{annee}.csv"
    dest.parent.mkdir(exist_ok=True)
    if not dest.exists():
        url = (f"https://raw.githubusercontent.com/JeffSackmann/"
               f"{REPOS[tour]}/master/{tour}_matches_{annee}.csv")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            print("  introuvable :", annee, e)
            return None
    return dest


if __name__ == "__main__":
    init_db()
    with SessionLocal() as s:
        for tour in REPOS:
            for a in ANNEES:
                p = telecharger(tour, a)
                if p:
                    print(tour, a, import_year(s, tour, p), "matchs")
    for tour in REPOS:
        run_db(tour)

