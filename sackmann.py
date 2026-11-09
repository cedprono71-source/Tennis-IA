"""Import des CSV de Jeff Sackmann (tennis_atp / tennis_wta).

Usage :
    python sackmann.py atp ./tennis_atp 2015 2025
    python sackmann.py wta ./tennis_wta 2015 2025
Fichiers attendus : {tour}_matches_{année}.csv
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

from db import SessionLocal, init_db
from models import Player, Tournament, Match


def _int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return None


def import_year(session, tour: str, path: Path):
    n = 0
    # On charge une fois ce qui existe déjà (évite des milliers de requêtes)
    known_players = {x[0] for x in session.query(Player.id).filter_by(tour=tour)}
    known_tourneys = {x[0] for x in session.query(Tournament.id).filter_by(tour=tour)}
    known_matches = {(x[0], x[1]) for x in session.query(Match.tourney_id, Match.match_num).filter_by(tour=tour)}
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                date = datetime.strptime(r["tourney_date"], "%Y%m%d").date()
            except (KeyError, ValueError):
                continue
            wid, lid = f"{tour}:{r['winner_id']}", f"{tour}:{r['loser_id']}"
            tid = f"{tour}:{r['tourney_id']}"

            for pid, pre in ((wid, "winner"), (lid, "loser")):
                if pid not in known_players:
                    known_players.add(pid)
                    session.add(Player(
                        id=pid, tour=tour, name=r[f"{pre}_name"],
                        hand=(r.get(f"{pre}_hand") or None),
                        height=_int(r.get(f"{pre}_ht")),
                        country=(r.get(f"{pre}_ioc") or None)))
            if tid not in known_tourneys:
                known_tourneys.add(tid)
                session.add(Tournament(
                    id=tid, tour=tour, name=r["tourney_name"],
                    surface=r.get("surface") or None,
                    level=r.get("tourney_level") or None,
                    best_of=_int(r.get("best_of"))))
            session.flush()

            mnum = _int(r.get("match_num"))
            if (tid, mnum) in known_matches:
                continue
            known_matches.add((tid, mnum))
            session.add(Match(
                tour=tour, tourney_id=tid, match_num=mnum, date=date,
                surface=r.get("surface") or None, round=r.get("round"),
                best_of=_int(r.get("best_of")), winner_id=wid, loser_id=lid,
                score=r.get("score"), minutes=_int(r.get("minutes")),
                **{f"{s}_{k.lower()}": _int(r.get(f"{s}_{k}"))
                   for s in ("w", "l")
                   for k in ("ace", "df", "svpt", "1stIn", "1stWon", "2ndWon")}))
            n += 1
    session.commit()
    return n


if __name__ == "__main__":
    tour, folder, y0, y1 = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    init_db()
    with SessionLocal() as s:
        for y in range(y0, y1 + 1):
            p = folder / f"{tour}_matches_{y}.csv"
            if p.exists():
                print(y, import_year(s, tour, p), "matchs")
