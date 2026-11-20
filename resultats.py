"""Ajoute les résultats récents (ESPN) à la base, puis recalcule l'Elo (ATP et WTA)."""
import time
import zlib
from datetime import timedelta

from sqlalchemy import func

import cotes
import espn
import predict
from db import SessionLocal, init_db
from elo import run_db
from models import Player, Tournament, Match
from suivi import aujourdhui

EXCLUS = ("walkover", "cancel", "postpon", "suspend", "default")


def _score(sc_w, sc_l):
    return " ".join(f"{a}-{b}" for a, b in zip(sc_w, sc_l))


def _joueur(s, tour, nom, cache):
    """Id du joueur : on le retrouve dans la base (même nom de famille + initiale), sinon on le crée."""
    if (tour, nom) in cache:
        return cache[(tour, nom)]
    mots = cotes._norm(nom)
    pid = None
    if mots:
        cands = s.query(Player).filter(Player.tour == tour, Player.name.ilike(f"%{mots[-1]}%")).all()
        ok = [p for p in cands if cotes.meme_joueur(nom, p.name)]
        if len(ok) > 1:
            ok.sort(key=lambda p: s.query(func.max(Match.id)).filter(
                (Match.winner_id == p.id) | (Match.loser_id == p.id)).scalar() or 0, reverse=True)
        if ok:
            pid = ok[0].id
    if pid is None:
        pid = f"{tour}:espn:{'-'.join(mots) or nom}"
        if not s.get(Player, pid):
            s.add(Player(id=pid, tour=tour, name=nom))
            s.flush()
    cache[(tour, nom)] = pid
    return pid


def _debut(s, tour):
    pref = f"{tour}:espn:%"
    d = s.query(func.max(Match.date)).filter(Match.tour == tour, Match.tourney_id.like(pref)).scalar()
    if d:
        return d - timedelta(days=3)  # on repasse sur les derniers jours : les doublons sont ignorés
    d = s.query(func.max(Match.date)).filter(Match.tour == tour).scalar()
    return d or (aujourdhui() - timedelta(days=30))


def importer(s, tour, log=print):
    pref, fin, cache = f"{tour}:espn:%", aujourdhui(), {}
    debut = max(_debut(s, tour), fin - timedelta(days=400))
    connus = {(t, n) for t, n in s.query(Match.tourney_id, Match.match_num).filter(
        Match.tour == tour, Match.tourney_id.like(pref))}
    # matchs déjà présents dans les données d'origine (évite de les compter deux fois)
    anciens = {(w, l) for w, l in s.query(Match.winner_id, Match.loser_id).filter(
        Match.tour == tour, ~Match.tourney_id.like(pref), Match.date >= debut - timedelta(days=21))}
    tournois = {t.id: t for t in s.query(Tournament).filter(Tournament.tour == tour, Tournament.id.like(pref))}
    n, jour = 0, debut
    while jour <= fin:
        try:
            ms = espn.matchs_du_jour(tour, jour)
        except Exception as ex:  # noqa: BLE001
            log(f"{tour} {jour} : {ex!r}")
            ms = []
        espn._CACHE.clear()
        for m in ms:
            st = (m["statut"] or "").lower()
            if m["etat"] != "post" or m["gagnant"] is None or any(x in st for x in EXCLUS) or not m["scores"][0]:
                continue
            tid = f"{tour}:espn:{m.get('event_id')}"
            num = zlib.crc32(str(m.get("match_id") or (m["a"] + m["b"])).encode()) & 0x7FFFFFFF
            if (tid, num) in connus:
                continue
            w, l = (0, 1) if m["gagnant"] == 0 else (1, 0)
            nom = (m["a"], m["b"])
            wid, lid = _joueur(s, tour, nom[w], cache), _joueur(s, tour, nom[l], cache)
            if (wid, lid) in anciens:
                continue
            if tid not in tournois:
                surf, bo = predict.auto_format(tour, m["tournoi"])
                tournois[tid] = Tournament(id=tid, tour=tour, name=m["tournoi"], surface=surf, level=None, best_of=bo)
                s.add(tournois[tid])
                s.flush()
            t = tournois[tid]
            s.add(Match(tour=tour, tourney_id=tid, match_num=num, date=jour, surface=t.surface,
                        round=(m.get("tour_tableau") or "")[:10], best_of=t.best_of,
                        winner_id=wid, loser_id=lid, score=_score(m["scores"][w], m["scores"][1 - w])))
            connus.add((tid, num))
            n += 1
        if jour.day % 10 == 0:
            s.commit()
        jour += timedelta(days=1)
        time.sleep(0.15)
    s.commit()
    log(f"{tour} : {n} nouveaux resultats ajoutes (du {debut} au {fin})")
    return n


def tout(log=print):
    init_db()
    total = 0
    with SessionLocal() as s:
        for tour in ("atp", "wta"):
            total += importer(s, tour, log)
    if total:
        for tour in ("atp", "wta"):
            log("Recalcul Elo " + tour + " : " + str(run_db(tour)))
    else:
        log("Rien de nouveau : Elo inchange")
    return total

