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

elo_ratings = {}

def get_elo(player_name):
    if player_name not in elo_ratings:
        elo_ratings[player_name] = 1500.0
    return elo_ratings[player_name]

def update_elo(winner, loser, k=32):
    w_elo = get_elo(winner)
    l_elo = get_elo(loser)

    exp_winner = 1 / (1 + 10 ** ((l_elo - w_elo) / 400))
    exp_loser = 1 / (1 + 10 ** ((w_elo - l_elo) / 400))

    elo_ratings[winner] = w_elo + k * (1 - exp_winner)
    elo_ratings[loser] = l_elo + k * (0 - exp_loser)

df["tourney_date"] = pd.to_datetime(df["tourney_date"], format="%Y%m%d")
df = df.sort_values("tourney_date").reset_index(drop=True)

for _, row in df.iterrows():
    update_elo(row["winner_name"], row["loser_name"])

sorted_players = sorted(elo_ratings.items(), key=lambda x: x[1], reverse=True)

print("— Top 5 des joueurs (Classement Elo 2024) —")
for player, elo in sorted_players[:5]:
    print(f"{player} : {round(elo, 1)}")

