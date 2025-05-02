from fonction_commune_chahid import *

# Charger les données
match = lire_csv("data/Match.csv")
player = lire_csv("data/Player.csv")
team = lire_csv("data/Team.csv")
match = match[(match["goal"].notna()) & (match["goal"] != "")]
goals_df = [transforme(g) for g in match["goal"]]


team_players = defaultdict(lambda: [set(), set()])

for df in goals_df:
    if "team" in df.columns and "player1" in df.columns and "player2" in df.columns:
        for _, row in df.iterrows():
            team = str(row["team"])

            # Ajout du buteur (si non nul)
            if pd.notna(row["player1"]):
                team_players[team][0].add(row["player1"])

            # Ajout du passeur décisif (si non nul)
            if pd.notna(row["player2"]):
                team_players[team][1].add(row["player2"])

# Calcul des stats finales
team_stats = {}
for team, (scorers, assisters) in team_players.items():
    team_stats[team] = [len(scorers), len(assisters)]

# Exemple d'affichage
for team, stats in team_stats.items():
    print(
        f"Équipe {team} : {stats[0]} buteurs distincts, {stats[1]} passeurs distincts"
    )

print(len(team_stats))
