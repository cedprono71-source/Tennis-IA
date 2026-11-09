import io
import pandas as pd
import requests

url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_matches_2024.csv"
response = requests.get(url)

if response.status_code == 200:
    df = pd.read_csv(io.StringIO(response.content.decode("utf-8")))
else:
    print("Erreur de téléchargement des données.")
    exit()

# Dictionnaire pour stocker l'Elo par surface : {joueur: {'Hard': 1500, 'Clay': 1500, 'Grass': 1500}}
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

df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d")
df = df.sort_values("tourney_date").reset_index(drop=True)

for _, row in df.iterrows():
    update_surface_elo(row["winner_name"], row["loser_name"], row["surface"])

# Affichage du Top 5 sur Terre battue (Clay)
clay_sorted = sorted(players_elo.items(), key=lambda x: x[1]["Clay"], reverse=True)

print("— Top 5 sur Terre battue (Clay) —")
for player, elos in clay_sorted[:5]:
    print(f"{player} : {round(elos['Clay'], 1)}")

