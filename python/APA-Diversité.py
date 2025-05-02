from fonction_commune_chahid import *


def diversite(season):
    # Charger les données
    match = lire_csv("data/Match.csv")
    player = lire_csv("data/Player.csv")
    team = lire_csv("data/Team.csv")
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == season]
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

    team_contributors = {}
    for team, (scorers, assisters) in team_players.items():
        contributors = scorers.union(assisters)
        team_contributors[team] = len(contributors)

    # Exemple d'affichage
    for team in team_contributors:
        print(
            f"Équipe {team} : {team_stats[team][0]} buteurs, {team_stats[team][1]} passeurs, {team_contributors[team]} contributeurs uniques"
        )

    print(f"Nombre total d'équipes : {len(team_contributors)}")


diversite("2014/2015")
