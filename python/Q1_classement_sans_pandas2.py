from fonction_commune_chahid import *

Team = lire_csv("data/Team.csv")
Match = lire_csv("data/Match.csv")

id_en_nom(Match, Team)

stats = creer_dict_2(["point", "scored", "conceded"])

for index, row in Match.iterrows():
    league_id = row["league_id"]
    season = row["season"]

    if league_id == 1729 and season == "2014/2015":
        home_team = row["home_team"]
        away_team = row["away_team"]
        home_goals = row["home_team_goal"]
        away_goals = row["away_team_goal"]

        # Mise à jour des buts marqués et encaissés
        stats[home_team]["scored"] += home_goals
        stats[home_team]["conceded"] += away_goals
        stats[away_team]["scored"] += away_goals
        stats[away_team]["conceded"] += home_goals

        # Attribution des points
        if home_goals > away_goals:  # Victoire équipe à domicile
            stats[home_team]["point"] += 3
        elif home_goals < away_goals:  # Victoire équipe à l'extérieur
            stats[away_team]["point"] += 3
        else:  # Match nul
            stats[home_team]["point"] += 1
            stats[away_team]["point"] += 1

stats = trier_dict(stats, ["point"], True)
