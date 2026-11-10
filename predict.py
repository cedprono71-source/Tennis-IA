"""Pronostic d'un match : Elo + stats de service + simulateur."""
from sqlalchemy import or_, func

from db import SessionLocal
from models import Player, Match, EloRating
from elo import expected, W_SURFACE
from simulator import calibrer, resume

SERVE_AVG = {"atp": 0.645, "wta": 0.565}   # points gagnés au service, moyenne du circuit
K_REGRESSION = 500                          # points "fictifs" ramenant vers la moyenne
SURFACES = {"hard": "Hard", "clay": "Clay", "grass": "Grass", "carpet": "Carpet"}


def trouver_joueur(s, tour, nom):
    cands = s.query(Player).filter(Player.tour == tour, Player.name.ilike(f"%{nom}%")).all()
    if not cands and " " in nom.strip():  # accents / prénoms différents : nom de famille
        cands = s.query(Player).filter(Player.tour == tour,
                                       Player.name.ilike(f"%{nom.strip().split()[-1]}%")).all()
    best, best_id = None, -1
    for p in cands:  # en cas d'homonymes : le plus récemment actif
        last = s.query(func.max(EloRating.id)).filter(EloRating.player_id == p.id).scalar() or 0
        if last > best_id:
            best, best_id = p, last
    return best


def elo_courant(s, pid, surface):
    g = s.query(EloRating.elo_global).filter(EloRating.player_id == pid) \
        .order_by(EloRating.id.desc()).first()
    sf = s.query(EloRating.elo_surface).filter(EloRating.player_id == pid, EloRating.surface == surface) \
        .order_by(EloRating.id.desc()).first()
    return (g[0] if g else 1500.0), (sf[0] if sf else 1500.0)


def _agreger(rows, pid):
    sv = won = osv = ret = 0
    for m in rows:
        if m.winner_id == pid:
            a, b, c, d = m.w_svpt, (m.w_1stwon or 0) + (m.w_2ndwon or 0), m.l_svpt, (m.l_1stwon or 0) + (m.l_2ndwon or 0)
        else:
            a, b, c, d = m.l_svpt, (m.l_1stwon or 0) + (m.l_2ndwon or 0), m.w_svpt, (m.w_1stwon or 0) + (m.w_2ndwon or 0)
        if not a or not c:
            continue
        sv, won, osv, ret = sv + a, won + b, osv + c, ret + (c - d)
    return sv, won, osv, ret


def stats_service(s, pid, surface, avg):
    """(proba de gagner un point au service, au retour, nb de matchs utilisés)."""
    base = s.query(Match).filter(or_(Match.winner_id == pid, Match.loser_id == pid),
                                 Match.w_svpt.isnot(None), Match.l_svpt.isnot(None))
    rows = base.filter(Match.surface == surface).order_by(Match.date.desc()).limit(40).all()
    if len(rows) < 15:
        rows = base.order_by(Match.date.desc()).limit(60).all()
    sv, won, osv, ret = _agreger(rows, pid)
    avg_r = 1 - avg
    s_adj = (won + avg * K_REGRESSION) / (sv + K_REGRESSION)
    r_adj = (ret + avg_r * K_REGRESSION) / (osv + K_REGRESSION)
    return s_adj, r_adj, len(rows)


def pronostic(tour, nom_a, nom_b, surface="Hard", best_of=3, ligne=None):
    tour = tour.lower()
    if tour not in SERVE_AVG:
        return {"erreur": "tour doit etre atp ou wta"}
    surface = SURFACES.get(surface.lower(), "Hard")
    avg = SERVE_AVG[tour]
    with SessionLocal() as s:
        A, B = trouver_joueur(s, tour, nom_a), trouver_joueur(s, tour, nom_b)
        if not A or not B:
            return {"erreur": f"joueur introuvable : {nom_a if not A else nom_b}"}
        ga, sa = elo_courant(s, A.id, surface)
        gb, sb = elo_courant(s, B.id, surface)
        p_elo = expected((1 - W_SURFACE) * ga + W_SURFACE * sa,
                         (1 - W_SURFACE) * gb + W_SURFACE * sb)
        s_a, r_a, n_a = stats_service(s, A.id, surface, avg)
        s_b, r_b, n_b = stats_service(s, B.id, surface, avg)

    # proba de gagner un point sur son propre service, contre cet adversaire
    pa = min(max(avg + (s_a - avg) - (r_b - (1 - avg)), 0.45), 0.85)
    pb = min(max(avg + (s_b - avg) - (r_a - (1 - avg)), 0.45), 0.85)
    pa_c, pb_c = calibrer(pa, pb, p_elo, best_of)  # cale la proba de victoire sur l'Elo
    lignes = [ligne - 1, ligne, ligne + 1] if ligne is not None else None
    out = resume(pa_c, pb_c, best_of, lignes)
    out.update({
        "match": f"{A.name} vs {B.name}", "surface": surface, "format": f"{best_of} sets gagnants" if best_of == 5 else "3 sets",
        "proba_victoire_elo": {A.name: round(p_elo, 4), B.name: round(1 - p_elo, 4)},
        "points_au_service": {A.name: round(pa_c, 3), B.name: round(pb_c, 3)},
        "matchs_utilises": {A.name: n_a, B.name: n_b},
    })
    out.pop("proba_A", None)
    if ligne is not None:
        o = out["over"][str(ligne)]
        out["pronostic_ligne"] = {"ligne": ligne, "over": o, "under": round(1 - o, 4)}
    return out
