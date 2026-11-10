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
    if dest.exists() and dest.stat().st_size > 1000:
        return dest
    repo, f = REPOS[tour], f"{tour}_matches_{annee}.csv"
    urls = [
        f"https://raw.githubusercontent.com/JeffSackmann/{repo}/master/{f}",
        f"https://raw.githubusercontent.com/JeffSackmann/{repo}/refs/heads/master/{f}",
        f"https://raw.githubusercontent.com/JeffSackmann/{repo}/main/{f}",
        f"https://github.com/JeffSackmann/{repo}/raw/master/{f}",
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
            erreurs.append(f"{url.split('/')[2]}...{url.split('/')[-2]} -> {e}")
    log(f"{tour} {annee} introuvable : " + " | ".join(erreurs[:2]))
    return None


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
