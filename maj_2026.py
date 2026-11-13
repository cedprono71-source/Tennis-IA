"""Ajoute les matchs 2026 puis recalcule les notes Elo."""
from db import SessionLocal, init_db
from setup_data import telecharger, elargir_colonnes, REPOS
from sackmann import import_year
from elo import run_db

ANNEE = 2026

if __name__ == "__main__":
    init_db()
    elargir_colonnes()
    with SessionLocal() as s:
        for tour in REPOS:
            p = telecharger(tour, ANNEE, print)
            if p:
                print(tour, ANNEE, ":", import_year(s, tour, p, print), "nouveaux matchs")
    for tour in REPOS:
        print(run_db(tour))
    print("TERMINE")
