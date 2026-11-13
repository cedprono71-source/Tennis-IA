"""Programme des matchs de tennis (ATP / WTA) depuis le flux public d'ESPN."""
import json
import time
import urllib.request
from datetime import datetime, date
from datetime import timezone, timedelta
try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo("Europe/Paris")
except Exception:  # base des fuseaux absente : on prend UTC+1
    TZ = timezone(timedelta(hours=1))
_CACHE = {}


def _get(tour, jour):
    cle = (tour, jour)
    if cle in _CACHE and time.time() - _CACHE[cle][0] < 300:
        return _CACHE[cle][1]
    url = f"https://site.api.espn.com/apis/site/v2/sports/tennis/{tour}/scoreboard?dates={jour}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8"))
    _CACHE[cle] = (time.time(), data)
    return data


def _nom(k):
    a = k.get("athlete") or {}
    return a.get("displayName") or a.get("fullName") or a.get("shortName")


def _parse_match(c, tournoi, tour):
    comps = c.get("competitors") or []
    if len(comps) != 2:
        return None
    comps = sorted(comps, key=lambda k: k.get("order", 0))
    noms = [_nom(k) for k in comps]
    if not all(noms):
        return None  # double ou joueur inconnu
    st = (c.get("status") or {}).get("type") or {}
    scores = []
    for k in comps:
        ls = k.get("linescores") or []
        scores.append([int(x.get("value")) for x in ls if x.get("value") is not None])
    return {
        "tour": tour,
        "tournoi": tournoi,
        "tour_tableau": (c.get("round") or {}).get("displayName") or "",
        "heure_utc": c.get("date") or c.get("startDate"),
        "statut": st.get("description") or "",
        "etat": st.get("state") or "",  # pre / in / post
        "a": noms[0], "b": noms[1],
        "gagnant": next((i for i, k in enumerate(comps) if k.get("winner")), None),
        "scores": scores,
    }


def matchs_du_jour(tour, jour: date):
    data = _get(tour, jour.strftime("%Y%m%d"))
    out = []
    for ev in data.get("events", []):
        tournoi = ev.get("name") or ev.get("shortName") or ""
        blocs = []
        for g in ev.get("groupings") or []:
            gi = g.get("grouping") or {}
            etiquette = (gi.get("slug", "") + gi.get("displayName", "")).lower()
            if "double" in etiquette:
                continue
            # Le flux peut mélanger hommes et femmes : on garde seulement le bon circuit.
            femme = "women" in etiquette
            homme = ("men" in etiquette) and not femme
            if (tour == "atp" and femme) or (tour == "wta" and homme):
                continue
            blocs += g.get("competitions") or []
        if not ev.get("groupings"):
            blocs = ev.get("competitions") or []
        for c in blocs:
            m = _parse_match(c, tournoi, tour)
            if not m:
                continue
            if m["heure_utc"]:
                try:
                    h = datetime.fromisoformat(m["heure_utc"].replace("Z", "+00:00")).astimezone(TZ)
                except ValueError:
                    h = None
                if h is not None and h.date() != jour:
                    continue
                m["heure"] = h.strftime("%H:%M") if h else ""
            else:
                m["heure"] = ""
            out.append(m)
    out.sort(key=lambda m: (m["heure_utc"] or "", m["tournoi"]))
    return out


def brut(tour, jour: date, n=4000):
    return json.dumps(_get(tour, jour.strftime("%Y%m%d")))[:n]
