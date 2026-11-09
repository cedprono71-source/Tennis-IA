import io
import pandas as pd
import requests

players_elo = {}

def get_elo(player_name, surface):
    if player_name not in players_elo:
        players_elo[player_name] = {"Hard": 1500.0, "Clay": 1500.0, "Grass": 1500.0}
    if surface not in players_elo[player_name]:
        players_elo[player_name][surface] = 1500.0
    return players_elo[player_name][surface]

def update_surface_elo(winner, loser, surface, k=32):
    if surface not in ["Hard", "Clay", "Grass"]:
        return

    w_elo = get_elo(winner, surface)
    l_elo = get_elo(loser, surface)

    exp_winner = 1 / (1 + 10 ** ((l_elo - w_elo) / 400))
    exp_loser = 1 / (1 + 10 ** ((w_elo - l_elo) / 400))

    players_elo[winner][surface] = w_elo + k * (1 - exp_winner)
    players_elo[loser][surface] = l_elo + k * (0 - exp_loser)

# Traitement sur plusieurs années pour consolider l'historique
years = [2022, 2023, 2024]

for year in years:
    url = f"https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_{year}.csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.content.decode("utf-8")))
        df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d")
        df = df.sort_values("tourney_date").reset_index(drop=True)

        for _, row in df.iterrows():
            update_surface_elo(row["winner_name"], row["loser_name"], row["surface"])

def predict_match(player1, player2, surface):
    p1_elo = get_elo(player1, surface)
    p2_elo = get_elo(player2, surface)

    prob_p1 = 1 / (1 + 10 ** ((p2_elo - p1_elo) / 400))
    prob_p2 = 1 - prob_p1

    print(f"— Prédiction sur {surface} (1822-2024) —")
    print(f"{player1} ({round(p1_elo)} Elo) : {round(prob_p1 * 100, 1)} %")
    print(f"{player2} ({round(p2_elo)} Elo) : {round(prob_p2 * 100, 1)} %")

predict_match("Jannik Sinner", "Carlos Alcaraz", "Hard")
