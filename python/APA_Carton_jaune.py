from fonction_commune_chahid import *


def carton_jaune(season):
    # Charger les données
    match = lire_csv("data/Match.csv")
    player = lire_csv("data/Player.csv")

    # Filtrer le championnat et la saison souhaités
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == season]

    card_df = [transforme(g) for g in match["card"]]
    team_stats = creer_dict(2)  # d = {Id_team = [Nombre carton Jaune, Nombre de Match]}

    if "home_team_api_id" in match.columns and "away_team_api_id" in match.columns:
        for _, row in match.iterrows():
            home = str(row["home_team_api_id"])
            away = str(row["away_team_api_id"])
            team_stats[home][1] += 1
            team_stats[away][1] += 1

    for df in card_df:
        if "team" in df.columns and "card_type" in df.columns:
            # Comptage des cartons jaunes
            yellow_cards = df[df["card_type"] == "y"]
            for team in yellow_cards["team"]:
                team_stats[str(team)][0] += 1  # +1 carton jaune

    for team in team_stats:
        Nb_Carton = team_stats[team][0]
        Nb_Match = team_stats[team][1]
        team_stats[team].append(round(Nb_Carton / Nb_Match, 2))

    # Exemple d'affichage
    for team, stats in team_stats.items():
        print(
            f"Équipe {team} : {stats[0]} cartons jaunes, {stats[1]} matchs, soit un ratio de {stats[2]} cartons jaunes par match"
        )


carton_jaune("2014/2015")
