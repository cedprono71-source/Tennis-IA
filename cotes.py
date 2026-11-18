"""Cotes des bookmakers français (Winamax, Betclic, Unibet, PMU, NetBet) via The Odds API.
Un pronostic n'est « jouable » que si un bookmaker français a une cote dessus."""
import json
import os
import re
import unicodedata
import urllib.request
from datetime import datetime, timedelta

from db import SessionLocal
from models import Cote

BASE = "https://api.the-odds-api.com/v4"
NOMS = {"winamax_fr": "Winamax", "betclic_fr": "Betclic", "unibet_fr": "Unibet",
        "pmu_fr": "PMU", "netbet_fr": "NetBet"}


# ---------- fonctions pures (testables sans base) ----------
def _norm(nom):
    t = unicodedata.normalize("NFKD", nom or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]", " ", t.replace("-", " ")).split()


def meme_joueur(x, y):
    """Même joueur ? Nom de famille identique + même initiale du prénom."""
    tx, ty = _norm(x), _norm(y)
    if not tx or not ty:
        return False
    if tx == ty:
        return True
    return tx[-1] == ty[-1] and tx[0][0] == ty[0][0]


def lire_evenement(ev):
    """Transforme un événement The Odds API en dictionnaire simple."""
    h2h, totals = {}, {}
    for bk in ev.get("bookmakers", []):
        k = bk.get("key")
        for mk in bk.get("markets", []):
            if mk.get("key") == "h2h":
                h2h[k] = {o["name"]: o["price"] for o in mk.get("outcomes", [])}
            elif mk.get("key") == "totals":
                for o in mk.get("outcomes", []):
                    if o.get("point") is None:
                        continue
                    totals.setdefault(str(float(o["point"])), {}).setdefault(k, {})[o["name"].lower()] = o["price"]
    return {"home": ev.get("home_team"), "away": ev.get("away_team"), "h2h": h2h, "totals": totals}


def _meilleur(prix_par_book):
    """prix_par_book : {book: cote}. Renvoie {'cote', 'book'} de la meilleure cote."""
    if not prix_par_book:
        return None
    b, c = max(prix_par_book.items(), key=lambda kv: kv[1])
    return {"cote": round(c, 2), "book": NOMS.get(b, b)}


def meilleures_cotes(d, a, b):
    """Meilleures cotes françaises pour le match a vs b, ou None si le match n'est pas coté."""
    if meme_joueur(a, d["home"]) and meme_joueur(b, d["away"]):
        na, nb = d["home"], d["away"]
    elif meme_joueur(a, d["away"]) and meme_joueur(b, d["home"]):
        na, nb = d["away"], d["home"]
    else:
        return None
    pa = {bk: p[na] for bk, p in d["h2h"].items() if na in p}
    pb = {bk: p[nb] for bk, p in d["h2h"].items() if nb in p}
    if not pa or not pb:
        return None
    totaux = []
    for ligne, books in sorted(d["totals"].items(), key=lambda kv: float(kv[0])):
        over = _meilleur({bk: v["over"] for bk, v in books.items() if "over" in v})
        under = _meilleur({bk: v["under"] for bk, v in books.items() if "under" in v})
        if over and under:
            totaux.append({"ligne": float(ligne), "over": over, "under": under})
    return {"a": _meilleur(pa), "b": _meilleur(pb), "totaux": totaux}


# ---------- base de données ----------
def table_remplie(s):
    return s.query(Cote.id).filter(Cote.tour != "meta").first() is not None


def charger(s, tour, jour):
    """Cotes (dict) des matchs de ce circuit autour de ce jour."""
    d0 = datetime(jour.year, jour.month, jour.day) - timedelta(days=1)
    rows = s.query(Cote.donnees).filter(Cote.tour == tour, Cote.debut >= d0,
                                        Cote.debut <= d0 + timedelta(days=3)).all()
    return [json.loads(r[0]) for r in rows]


def chercher(liste, a, b):
    for d in liste:
        r = meilleures_cotes(d, a, b)
        if r:
            return r
    return None


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode()), r.headers.get("x-requests-remaining")


def maj_cotes(min_heures=6, force=False):
    """Récupère les cotes françaises (au plus toutes les `min_heures` pour ménager les crédits)."""
    cle = os.getenv("ODDS_API_KEY")
    if not cle:
        return "ODDS_API_KEY absente"
    now = datetime.utcnow()
    with SessionLocal() as s:
        meta = s.query(Cote).filter_by(event_id="__meta__").first()
        if meta and not force and (now - meta.maj) < timedelta(hours=min_heures):
            return "cotes recentes, rien a faire"
        sports, _ = _get(f"{BASE}/sports/?apiKey={cle}")
        actifs = [x["key"] for x in sports if x["key"].startswith("tennis_") and x.get("active")]
        n, restant = 0, None
        for k in actifs:
            try:
                evs, restant = _get(f"{BASE}/sports/{k}/odds?apiKey={cle}&regions=fr"
                                    f"&markets=h2h,totals&oddsFormat=decimal&dateFormat=iso")
            except Exception:
                continue
            tour = "wta" if "_wta_" in k else "atp"
            for ev in evs:
                d = lire_evenement(ev)
                if not d["h2h"]:
                    continue
                debut = datetime.fromisoformat(ev["commence_time"].replace("Z", "+00:00")).replace(tzinfo=None)
                row = s.query(Cote).filter_by(event_id=ev["id"]).first()
                if row:
                    row.donnees, row.maj, row.debut = json.dumps(d), now, debut
                else:
                    s.add(Cote(event_id=ev["id"], tour=tour, debut=debut, maj=now, donnees=json.dumps(d)))
                n += 1
            s.commit()
            if restant is not None and float(restant) < 15:
                break
        if meta:
            meta.maj = now
        else:
            s.add(Cote(event_id="__meta__", tour="meta", debut=None, maj=now, donnees="{}"))
        s.query(Cote).filter(Cote.debut < now - timedelta(days=3)).delete()
        s.commit()
    return f"{n} matchs cotes ({len(actifs)} tournois), credits restants : {restant}"

