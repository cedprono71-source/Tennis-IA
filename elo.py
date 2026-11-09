"""Elo global + par surface, avec backtest.

Le cœur (EloEngine) est sans base de données : testable seul.
Usage :  python -m app.elo atp
"""
import math
import sys
from collections import defaultdict

START = 1500.0
W_SURFACE = 0.5  # poids Elo surface dans la proba finale


def expected(ra: float, rb: float) -> float:
    return 1.0 / (1.0 + 10 ** ((rb - ra) / 400.0))


def k_factor(n_matches: int) -> float:
    # K décroissant avec l'expérience (style FiveThirtyEight)
    return 250.0 / ((n_matches + 5) ** 0.4)


class EloEngine:
    def __init__(self):
        self.g = defaultdict(lambda: START)      # Elo global
        self.s = defaultdict(lambda: START)      # Elo par (joueur, surface)
        self.n = defaultdict(int)                # matchs joués (global)
        self.ns = defaultdict(int)               # matchs joués par surface

    def rating(self, p, surface):
        return (1 - W_SURFACE) * self.g[p] + W_SURFACE * self.s[(p, surface)]

    def win_prob(self, a, b, surface) -> float:
        return expected(self.rating(a, surface), self.rating(b, surface))

    def update(self, winner, loser, surface):
        """Met à jour après un match. Renvoie la proba pré-match du vainqueur."""
        p = self.win_prob(winner, loser, surface)
        for ratings, key_w, key_l, nw, nl in (
            (self.g, winner, loser, self.n[winner], self.n[loser]),
            (self.s, (winner, surface), (loser, surface),
             self.ns[(winner, surface)], self.ns[(loser, surface)]),
        ):
            e = expected(ratings[key_w], ratings[key_l])
            ratings[key_w] += k_factor(nw) * (1 - e)
            ratings[key_l] -= k_factor(nl) * (1 - e)
        for key in (winner, loser):
            self.n[key] += 1
        for key in (winner, loser):
            self.ns[(key, surface)] += 1
        return p


def run_backtest(matches):
    """matches : itérable (winner_id, loser_id, surface) trié par date.
    Les proba sont calculées AVANT mise à jour (pas de fuite de données)."""
    eng, ll, ok, n = EloEngine(), 0.0, 0, 0
    for w, l, surf in matches:
        p = eng.update(w, l, surf or "Hard")
        if eng.n[w] > 10 and eng.n[l] > 10:  # ignore les débuts de carrière
            ll += -math.log(max(p, 1e-9))
            ok += p > 0.5
            n += 1
    return eng, {"matchs": n, "accuracy": ok / n if n else None,
                 "log_loss": ll / n if n else None}


def run_db(tour: str):
    from app.db import SessionLocal, init_db
    from app.models import Match, EloRating
    init_db()
    with SessionLocal() as s:
        s.query(EloRating).filter(
            EloRating.match_id.in_(s.query(Match.id).filter_by(tour=tour))
        ).delete(synchronize_session=False)
        rows = (s.query(Match).filter_by(tour=tour)
                .order_by(Match.date, Match.tourney_id, Match.match_num).all())
        eng = EloEngine()
        ll, ok, n = 0.0, 0, 0
        for m in rows:
            surf = m.surface or "Hard"
            p = eng.update(m.winner_id, m.loser_id, surf)
            if eng.n[m.winner_id] > 10 and eng.n[m.loser_id] > 10:
                ll += -math.log(max(p, 1e-9)); ok += p > 0.5; n += 1
            for pid in (m.winner_id, m.loser_id):
                s.add(EloRating(match_id=m.id, player_id=pid, date=m.date,
                                elo_global=eng.g[pid], elo_surface=eng.s[(pid, surf)],
                                surface=surf))
        s.commit()
        print(f"{tour.upper()} : {n} matchs | accuracy {ok/n:.3f} | log-loss {ll/n:.4f}")


if __name__ == "__main__":
    run_db(sys.argv[1] if len(sys.argv) > 1 else "atp")

