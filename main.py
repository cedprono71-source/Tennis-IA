import io
import pandas as pd
import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

players_elo = {}
data_loaded = False

def load_data():
    global data_loaded
    if data_loaded:
        return
    for year in [2022, 2023, 2024]:
        url = f"https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_{year}.csv"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.content.decode("utf-8")))
                df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d", errors="coerce")
                df = df.dropna(subset=["tourney_date"]).sort_values("tourney_date").reset_index(drop=True)
                for _, row in df.iterrows():
                    w, l, s = row.get("winner_name"), row.get("loser_name"), row.get("surface")
                    if pd.notna(w) and pd.notna(l) and pd.notna(s) and s in ["Hard", "Clay", "Grass"]:
                        if w not in players_elo: players_elo[w] = {"Hard": 1500.0, "Clay": 1500.0, "Grass": 1500.0}
                        if l not in players_elo: players_elo[l] = {"Hard": 1500.0, "Clay": 1500.0, "Grass": 1500.0}
                        w_elo, l_elo = players_elo[w][s], players_elo[l][s]
                        exp_w = 1 / (1 + 10 ** ((l_elo - w_elo) / 400))
                        exp_l = 1 / (1 + 10 ** ((w_elo - l_elo) / 400))
                        players_elo[w][s] = w_elo + 32 * (1 - exp_w)
                        players_elo[l][s] = l_elo + 32 * (0 - exp_l)
        except Exception:
            pass
    data_loaded = True

@app.get("/", response_class=HTMLResponse)
def home():
    load_data()
    hard_sorted = sorted(players_elo.items(), key=lambda x: x[1]["Hard"], reverse=True)[:5]
    ranking_html = "".join([f"<li>{player} — {round(elos['Hard'])} Elo (Hard)</li>" for player, elos in hard_sorted])

    return f"""
    <!DOCTYPE html>
    <html>
        <head><title>Tennis Elo</title><meta charset="utf-8"></head>
        <body style="font-family: Arial; max-width: 600px; margin: 40px auto; padding: 0 20px;">
            <h1>Modèle Elo Tennis</h1>
            <p>Serveur opérationnel.</p>
            <h2>Top 5 Joueurs (Surface Dure)</h2>
            <ul>{ranking_html if ranking_html else "<li>Calcul en cours...</li>"}</ul>
        </body>
    </html>
    """
