"""Complète la base avec les matchs terminés d'ESPN (depuis le dernier match connu),
puis recalcule les notes Elo.

Lancement : python maj_espn.py
"""
import re
import sys
import time
import unicodedata
import zlib
from datetime import datetime, timedelta

from sqlalchemy import func

from db import SessionLocal, init_db
from models import EloRating, Match, Player, Tournament
import espn
from elo import run_db

ANNULES = ("walkover", "cancel", "postpon", "suspend")
ARGILE = ("roland", "rome", "italia", "italian", "madrid", "monte carlo", "barcelona", "hamburg",
          "estoril", "geneva", "lyon", "marrakech", "bucharest", "munich", "houston", "buenos aires",
          "rio", "santiago", "cordoba", "gstaad", "bastad", "umag", "kitzbuhel", "bogota", "parma",
          "prague", "rabat", "strasbourg", "palermo", "lausanne", "warsaw", "bad gastein", "sao paulo",
          "french open", "charleston", "bordeaux", "belgrade", "cagliari", "bucarest",
          "generali open", "nordea open", "auvergne rhone alpes")
GAZON = ("wimbledon", "halle", "queen", "stuttgart", "hertogenbosch", "mallorca", "eastbourne",
         "newport", "berlin", "bad homburg", "nottingham", "birmingham", "surbiton", "libema",
         "boss open", "hsbc championships", "terra wortmann")
GRANDS_CHELEMS = ("wimbledon", "us open", "roland garros", "french open", "australian open")


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def code_tour(txt):
    t = norm(txt)
    if "semi" in t:
        return "SF"
    if "quarter" in t:
        return "QF"
    if "final" in t:
        return "F"
    m = re.search(r"round of (\d+)", t)
    if m:
        return "R" + m.group(1)
    if "robin" in t or "group" in t:
        return "RR"
    if "3rd" in t or "third" in t or "bronze" in t:
        return "BR"
    return t[:10] or None


def charger_tournois(s, tour):
    """Tournois de référence (import historique) : on exclut ceux créés depuis ESPN."""
    d = {}
    q = (s.query(Tournament.name, Tournament.surface, Tournament.level, Tournament.best_of)
         .filter(Tournament.tour == tour, ~Tournament.id.like("%-espn-%"))
         .order_by(Tournament.id))
    for nom, surf, lvl, bo in q:
        if nom and surf:
            d[norm(nom)] = (surf, lvl, bo)  # le plus récent écrase les anciens
    return d


def contient(n, mots):
    """Vrai si l'un des mots (ou expressions) apparaît en mots entiers dans n."""
    return any(re.search(r"\b" + re.escape(w) + r"\b", n) for w in mots)


def infos_tournoi(nom_espn, connus, tour):
    """Renvoie ((surface, niveau, best_of), source)."""
    n = norm(nom_espn)
    cands = [k for k in connus if k and (k in n or n in k)]
    if cands:
        return connus[max(cands, key=len)], "connu"
    if contient(n, ARGILE):
        surf = "Clay"
    elif contient(n, GAZON):
        surf = "Grass"
    else:
        surf = "Hard"
    if contient(n, GRANDS_CHELEMS):
        return (surf, "G", 5 if tour == "atp" else 3), "devine"
    return (surf, "A", 3), "devine"


def corriger_surfaces(s, tour, log=print):
    """Réapplique les règles de surface aux tournois déjà créés depuis ESPN."""
    connus = charger_tournois(s, tour)
    corriges = []
    q = s.query(Tournament).filter(Tournament.tour == tour, Tournament.id.like("%-espn-%"))
    for t in q.all():
        (surf, niveau, bo), _ = infos_tournoi(t.name, connus, tour)
        if surf != t.surface:
            corriges.append(f"{t.name}: {t.surface} -> {surf}")
            t.surface = surf
            s.query(Match).filter(Match.tourney_id == t.id).update({"surface": surf})
    s.commit()
    if corriges:
        log(f"{tour.upper()} : surfaces corrigees : " + " | ".join(corriges))


def importer(s, tour, log=print):
    joueurs = {norm(n): pid for pid, n in s.query(Player.id, Player.name).filter_by(tour=tour)}
    tournois = charger_tournois(s, tour)
    dernier = s.query(func.max(Match.date)).filter_by(tour=tour).scalar()
    if dernier is None:
        log(f"{tour} : base vide, lance d'abord l'import historique.")
        return 0
    debut = dernier - timedelta(days=3)
    aujourdhui = datetime.now(espn.TZ).date()
    anciens = {(w, l) for w, l in s.query(Match.winner_id, Match.loser_id).filter(
        Match.tour == tour, Match.date >= debut - timedelta(days=21))}
    # Joueurs connus de l'AUTRE circuit (import historique) : sert à écarter les matchs
    # hommes/femmes qui arrivent dans le mauvais flux ESPN.
    autre = "wta" if tour == "atp" else "atp"
    autres = {norm(nm) for (nm,) in s.query(Player.name).filter(
        Player.tour == autre, ~Player.id.like("%:espn:%"))}
    vus, nouveaux, devines, ignores = set(), [], {}, 0

    def joueur(nom):
        k = norm(nom)
        if k in joueurs:
            return joueurs[k]
        pid = f"{tour}:espn:{k.replace(' ', '-')}"
        joueurs[k] = pid
        s.add(Player(id=pid, tour=tour, name=nom))
        nouveaux.append(nom)
        return pid

    n = 0
    jour = debut
    while jour <= aujourdhui:
        try:
            matchs = espn.matchs_du_jour(tour, jour)
        except Exception as e:  # noqa: BLE001
            log(f"{tour} {jour} : ESPN indisponible ({e!r})")
            jour += timedelta(days=1)
            continue
        for m in matchs:
            g = m.get("gagnant")
            if m["etat"] != "post" or g not in (0, 1):
                continue
            if any(x in (m["statut"] or "").lower() for x in ANNULES):
                continue
            sc = m["scores"]
            if len(sc) != 2 or not sc[0] or not sc[1]:
                continue
            nom_g, nom_p = (m["a"], m["b"]) if g == 0 else (m["b"], m["a"])
            kg, kp = norm(nom_g), norm(nom_p)
            if (kg not in joueurs and kg in autres) or (kp not in joueurs and kp in autres):
                ignores += 1  # joueur d'un autre circuit : on n'importe pas
                continue
            wid, lid = joueur(nom_g), joueur(nom_p)
            if (wid, lid) in anciens or (jour, wid, lid) in vus:
                continue
            vus.add((jour, wid, lid))
            (surf, niveau, bo), source = infos_tournoi(m["tournoi"], tournois, tour)
            if source == "devine":
                devines[m["tournoi"]] = surf
            tid = f"{tour}:{jour.year}-espn-{norm(m['tournoi']).replace(' ', '-')}"
            if s.get(Tournament, tid) is None:
                s.add(Tournament(id=tid, tour=tour, name=m["tournoi"], surface=surf,
                                 level=niveau, best_of=bo))
            s.flush()
            score = " ".join(f"{x}-{y}" for x, y in zip(sc[g], sc[1 - g]))
            mnum = zlib.crc32(f"{jour}|{wid}|{lid}".encode()) % 1_000_000_000
            s.add(Match(tour=tour, tourney_id=tid, match_num=mnum, date=jour, surface=surf,
                        round=code_tour(m.get("tour_tableau")), best_of=bo,
                        winner_id=wid, loser_id=lid, score=score))
            n += 1
        s.commit()
        time.sleep(0.2)
        jour += timedelta(days=1)

    log(f"{tour.upper()} : {n} nouveaux matchs ajoutes (du {debut} au {aujourdhui}), "
        f"{ignores} ignores (autre circuit)")
    if nouveaux:
        extrait = sorted(set(nouveaux))
        log(f"{tour.upper()} : {len(extrait)} joueurs nouveaux ou noms non reconnus : "
            + ", ".join(extrait[:40]))
    if devines:
        log(f"{tour.upper()} : surface devinee pour : "
            + " | ".join(f"{t} -> {sf}" for t, sf in sorted(devines.items())))
    return n


def nettoyer_espn(s, log=print):
    """Supprime tout ce qui a été importé depuis ESPN (matchs, tournois, joueurs créés, notes liées)
    pour repartir proprement. L'import historique (Sackmann) n'est pas touché."""
    ids_matchs = s.query(Match.id).filter(Match.tourney_id.like("%-espn-%"))
    s.query(EloRating).filter(EloRating.match_id.in_(ids_matchs)).delete(synchronize_session=False)
    s.query(EloRating).filter(EloRating.player_id.like("%:espn:%")).delete(synchronize_session=False)
    n = s.query(Match).filter(Match.tourney_id.like("%-espn-%")).delete(synchronize_session=False)
    s.query(Tournament).filter(Tournament.id.like("%-espn-%")).delete(synchronize_session=False)
    p = s.query(Player).filter(Player.id.like("%:espn:%")).delete(synchronize_session=False)
    s.commit()
    log(f"Nettoyage ESPN : {n} matchs et {p} joueurs supprimes")


if __name__ == "__main__":
    init_db()
    if "--nettoyer" in sys.argv:
        with SessionLocal() as s:
            nettoyer_espn(s, print)
    with SessionLocal() as s:
        for tour in ("atp", "wta"):
            corriger_surfaces(s, tour, print)
            importer(s, tour, print)
    for tour in ("atp", "wta"):
        print(run_db(tour))
    print("TERMINE")
