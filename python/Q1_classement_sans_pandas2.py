from fonctions_communes import *

team_names = lire_csv_en_dict("data/Team.csv", "team_api_id", ("team_long_name"))

# Lecture du fichier des matchs et filtrage pour l'année 2014
matchs = lire_csv_en_dict(
    "data/Match.csv",
    "id",
    "season",
    "league_id",
    "home_team_api_id",
    "away_team_api_id",
    "home_team_goal",
    "away_team_goal",
)


# {team_id: [point, scored, conceded]}
stats = creer_dict(3)

matchs = filtre_dic(matchs, 0, "2014/2015")
matchs = filtre_dic(matchs, 1, "1729")

for match_id, match in matchs.items():
    home_team_id = match[2]
    away_team_id = match[3]
    home_goals = int(match[4])
    away_goals = int(match[5])

    for team_id in [home_team_id, away_team_id]:
        if team_id not in stats:
            stats[team_id] = [0, 0, 0]  # [points, goals_scored, goals_conceded]

    stats[home_team_id][1] += home_goals
    stats[home_team_id][2] += away_goals
    stats[away_team_id][1] += away_goals
    stats[away_team_id][2] += home_goals

    if home_goals > away_goals:
        stats[home_team_id][0] += 3
    elif home_goals < away_goals:
        stats[away_team_id][0] += 3
    else:
        stats[home_team_id][0] += 1
        stats[away_team_id][0] += 1


print(stats)

classement = sorted(stats.items(), key=lambda x: x[1][0], reverse=True)

# En-tête
print(f"{'Équipe':<30} {'Pts':<5} {'BM':<5} {'BE':<5}")

# Affichage
for team_id, (points, scored, conceded) in classement:
    nom = name_team_dic(team_names, team_id)
    print(f"{nom:<30} {points:<5} {scored:<5} {conceded:<5}")
