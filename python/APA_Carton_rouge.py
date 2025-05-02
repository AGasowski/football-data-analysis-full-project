from fonction_commune_chahid import *

# Charger les données
match = lire_csv("data/Match.csv")
player = lire_csv("data/Player.csv")

# Filtrer le championnat et la saison souhaités
match = match[(match["goal"].notna()) & (match["goal"] != "")]

card_df = [transforme(g) for g in match["card"]]

team_stats = creer_dict(2)  # d = {Id_team = [Nombre carton Jaune, Nombre de Match]}

for df in card_df:
    if "team" in df.columns and "card_type" in df.columns:
        # On récupère les équipes présentes dans ce match
        teams_in_match = set(df["team"])
        for team in teams_in_match:
            team_stats[str(team)][1] += 1  # +1 match joué

        # Comptage des cartons jaunes
        red_cards = df[df["card_type"] == "r"]
        for team in red_cards["team"]:
            team_stats[str(team)][0] += 1  # +1 carton jaune


for team in team_stats:
    Nb_Carton = team_stats[team][0]
    Nb_Match = team_stats[team][1]
    team_stats[team].append(round(Nb_Carton / Nb_Match, 1))


# Exemple d'affichage
for team, stats in team_stats.items():
    print(
        f"Équipe {team} : {stats[0]} cartons jaunes, {stats[1]} matchs, soit un ratio de {stats[2]} cartons jaunes par match"
    )
