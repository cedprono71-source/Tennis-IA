"""Télécharge les matchs ATP/WTA, les importe, puis calcule les notes Elo.
Peut être lancé en ligne de commande ou depuis le site (/setup)."""
import urllib.request
from pathlib import Path

from sqlalchemy import text
from db import SessionLocal, init_db, engine
from sackmann import import_year
from elo import run_db

ANNEES = range(2015, 2026)
REPOS = {"atp": "tennis_atp", "wta": "tennis_wta"}


def telecharger(tour, annee, log):
    dest = Path("data") / f"{tour}_matches_{annee}.csv"
    dest.parent.mkdir(exist_ok=True)
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    repo, f = REPOS[tour], f"{tour}_matches_{annee}.csv"
    urls = [
        # Copie de sauvegarde (le dépôt d'origine de Sackmann répond 404)
        f"https://raw.githubusercontent.com/Aneeshers/tennis-sackmann-archive/main/{tour}/{f}",
        f"https://huggingface.co/datasets/Aneeshers/tennis-sackmann-archive/resolve/main/{tour}/{f}",
        # Dépôt d'origine, au cas où il reviendrait
        f"https://raw.githubusercontent.com/JeffSackmann/{repo}/master/{f}",
    ]
    erreurs = []
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) > 1000:
                dest.write_bytes(data)
                return dest
            erreurs.append(f"trop petit ({len(data)} octets)")
        except Exception as e:
            erreurs.append(f"{url.split('/')[2]}/{url.split('/')[4]} -> {e}")
    log(f"{tour} {annee} introuvable : " + " | ".join(erreurs))
    return None


def elargir_colonnes():
    """Agrandit des colonnes déjà créées trop petites (ignoré si impossible)."""
    for table, col, typ in [("tournaments", "level", "VARCHAR(10)"),
                            ("tournaments", "surface", "VARCHAR(20)"),
                            ("matches", "surface", "VARCHAR(20)"),
                            ("matches", "round", "VARCHAR(10)"),
                            ("elo_ratings", "surface", "VARCHAR(20)"),
                            ("players", "hand", "VARCHAR(5)"),
                            ("players", "country", "VARCHAR(10)")]:
        try:
            with engine.begin() as c:
                c.execute(text(f"ALTER TABLE {table} ALTER COLUMN {col} TYPE {typ}"))
        except Exception:
            pass


def tout_faire(log=print):
    init_db()
    elargir_colonnes()
    with SessionLocal() as s:
        for tour in REPOS:
            for a in ANNEES:
                p = telecharger(tour, a, log)
                if p:
                    log(f"{tour} {a} : {import_year(s, tour, p, log)} matchs importes")
    for tour in REPOS:
        log("Calcul des notes " + tour + "...")
        log(run_db(tour))
    log("TERMINE")


if __name__ == "__main__":
    tout_faire()
