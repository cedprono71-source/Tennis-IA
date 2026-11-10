"""Simulateur de match de tennis (calcul exact, sans hasard).

On part de la proba de gagner un point quand on sert, pour chaque joueur,
puis on calcule : jeux -> sets -> match. Résultat : proba de victoire,
distribution du nombre total de jeux (over/under) et du nombre de sets.
Hypothèse simplifiée : tie-break à 6-6 dans tous les sets.
"""
from functools import lru_cache


def game_win(p: float) -> float:
    """Proba que le serveur gagne un jeu, sachant p = proba de gagner un point."""
    q = 1 - p
    pre = p**4 * (1 + 4 * q + 10 * q**2)          # gagne sans passer par 40-40
    deuce = 20 * p**3 * q**3 * (p**2 / (p**2 + q**2))
    return pre + deuce


def tiebreak_win(pa: float, pb: float) -> float:
    """Proba que A gagne le tie-break (A sert le 1er point).
    pa = proba pour A de gagner un point sur son service ; pb idem pour B."""
    def pa_pair():
        # À 6-6 (12 points joués) : A sert le point 13. Deux points consécutifs
        # sont servis par la même personne ; on joue des "mini-manches".
        # Proba A gagne 2 points d'affilée sur 2 points = (pa)(1-pb) (A sert 13, B sert 14)
        w = pa * (1 - pb)
        l = (1 - pa) * pb
        return w / (w + l)

    @lru_cache(None)
    def g(a, b):
        if a == 6 and b == 6:
            return pa_pair()
        if a >= 7 and a - b >= 2:
            return 1.0
        if b >= 7 and b - a >= 2:
            return 0.0
        n = a + b
        a_serves = ((n + 1) // 2) % 2 == 0
        p = pa if a_serves else 1 - pb
        # après 6-6, retour dans la boucle d'égalité : 7-6 ou 6-7 puis retour à 6-6
        if a >= 6 and b >= 6:
            # (7,6) ou (6,7) etc. : l'écart d'1 point revient à 6-6 ou finit
            if a > b:
                return p + (1 - p) * pa_pair()
            return p * pa_pair()
        return p * g(a + 1, b) + (1 - p) * g(a, b + 1)

    return g(0, 0)


def set_distribution(pa: float, pb: float, a_first: bool):
    """Distribution d'un set. pa/pb : proba de gagner un point à son service.
    Renvoie {(jeux_A, jeux_B): proba}."""
    hold_a, hold_b = game_win(pa), game_win(pb)
    tb = tiebreak_win(pa, pb) if a_first else 1 - tiebreak_win(pb, pa)
    # tie-break : le premier serveur du tie-break est le serveur du 13e jeu
    # = le premier serveur du set (12 jeux joués, nombre pair)
    res = {}
    layer = {(0, 0): 1.0}
    for total in range(0, 13):
        nxt = {}
        for (a, b), pr in layer.items():
            if a == 6 and b == 6:
                res[(7, 6)] = res.get((7, 6), 0) + pr * tb
                res[(6, 7)] = res.get((6, 7), 0) + pr * (1 - tb)
                continue
            if (a >= 6 and a - b >= 2) or (a == 7):
                res[(a, b)] = res.get((a, b), 0) + pr
                continue
            if (b >= 6 and b - a >= 2) or (b == 7):
                res[(a, b)] = res.get((a, b), 0) + pr
                continue
            a_serves = (total % 2 == 0) == a_first
            pw = hold_a if a_serves else 1 - hold_b
            nxt[(a + 1, b)] = nxt.get((a + 1, b), 0) + pr * pw
            nxt[(a, b + 1)] = nxt.get((a, b + 1), 0) + pr * (1 - pw)
        layer = nxt
    return res


def match_distribution(pa: float, pb: float, best_of: int = 3):
    """Calcule le match entier. A sert en premier.
    Renvoie (proba_A_gagne, {jeux_total: proba}, {(sets_A, sets_B): proba})."""
    need = best_of // 2 + 1
    sets = {True: set_distribution(pa, pb, True), False: set_distribution(pa, pb, False)}
    layer = {(0, 0, True, 0): 1.0}  # (setsA, setsB, A_sert_premier, jeux_total)
    p_win, games, scores = 0.0, {}, {}
    while layer:
        nxt = {}
        for (sa, sb, a_first, tot), pr in layer.items():
            for (ga, gb), q in sets[a_first].items():
                np_, nsa, nsb, ntot = pr * q, sa + (ga > gb), sb + (gb > ga), tot + ga + gb
                if nsa == need or nsb == need:
                    games[ntot] = games.get(ntot, 0) + np_
                    scores[(nsa, nsb)] = scores.get((nsa, nsb), 0) + np_
                    if nsa == need:
                        p_win += np_
                else:
                    nf = a_first if (ga + gb) % 2 == 0 else not a_first
                    k = (nsa, nsb, nf, ntot)
                    nxt[k] = nxt.get(k, 0) + np_
        layer = nxt
    return p_win, games, scores


def calibrer(pa: float, pb: float, p_cible: float, best_of: int = 3):
    """Décale les proba de service (+d pour A, -d pour B) pour que la proba de
    victoire de A colle à p_cible (par ex. celle donnée par l'Elo)."""
    lo, hi = -0.15, 0.15
    for _ in range(18):
        d = (lo + hi) / 2
        pw, _, _ = match_distribution(min(max(pa + d, 0.3), 0.95),
                                      min(max(pb - d, 0.3), 0.95), best_of)
        if pw < p_cible:
            lo = d
        else:
            hi = d
    d = (lo + hi) / 2
    return min(max(pa + d, 0.3), 0.95), min(max(pb - d, 0.3), 0.95)


def resume(pa, pb, best_of=3, lignes=None):
    pw, games, scores = match_distribution(pa, pb, best_of)
    esp = sum(g * p for g, p in games.items())
    if lignes is None:
        base = int(esp)
        lignes = [base - 2 + 0.5, base - 1 + 0.5, base + 0.5, base + 1.5, base + 2.5]
    over = {str(l): round(sum(p for g, p in games.items() if g > l), 4) for l in lignes}
    return {
        "proba_A": round(pw, 4),
        "jeux_attendus": round(esp, 2),
        "over": over,
        "sets": {f"{a}-{b}": round(p, 4) for (a, b), p in sorted(scores.items())},
    }

