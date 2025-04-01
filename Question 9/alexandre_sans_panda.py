import csv
from collections import defaultdict

# Chargement des noms des équipes
team_names = {}

with open("data/Team.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_id = int(row["team_api_id"])
        team_name = row["team_long_name"]
        team_names[team_id] = team_name  # Associer ID à nom

# Dictionnaires pour stocker les statistiques des buts
goals_home = defaultdict(
    lambda: [0, 0]
)  # {team_id: [total_buts_domicile, nb_matchs_domicile]}
goals_away = defaultdict(
    lambda: [0, 0]
)  # {team_id: [total_buts_exterieur, nb_matchs_exterieur]}

# Lecture du fichier des matchs et filtrage pour l'année 2014
with open("data/Match.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        match_date = row["date"][:4]  # Extraire l'année de la date
        if match_date != "2014":
            continue  # Ignorer les matchs hors de l'année 2014

        home_team = int(row["home_team_api_id"])
        away_team = int(row["away_team_api_id"])
        home_goals = int(row["home_team_goal"])
        away_goals = int(row["away_team_goal"])

        # Mise à jour des statistiques
        goals_home[home_team][0] += home_goals
        goals_home[home_team][1] += 1

        goals_away[away_team][0] += away_goals
        goals_away[away_team][1] += 1

# Calcul des moyennes et différences
team_performance = []

for team in goals_home.keys():
    home_avg = (
        goals_home[team][0] / goals_home[team][1]
        if goals_home[team][1] > 0
        else 0
    )
    away_avg = (
        goals_away[team][0] / goals_away[team][1]
        if goals_away[team][1] > 0
        else 0
    )
    diff = away_avg - home_avg  # Différence entre extérieur et domicile

    team_performance.append((team, home_avg, away_avg, diff))

# Classement des équipes par ordre décroissant de différence
team_performance.sort(key=lambda x: x[3], reverse=True)

# Affichage des 10 meilleures équipes
print(
    "Classement des équipes avec la plus grande différence de buts marqués à "
    "l'extérieur vs domicile (année 2014) :"
)
print("-" * 100)
print(
    f"{'Rang':<5}{'Équipe':<30}{'Moy. Buts Dom.':<18}{'Moy. Buts Ext.':<18}"
    f"{'Différence':<12}"
)
print("-" * 100)

for rank, (team_id, home_avg, away_avg, diff) in enumerate(
    team_performance[:10], start=1
):  # Top 10
    team_name = team_names.get(team_id, "Inconnu")  # Récupérer le nom
    print(
        f"{rank:<5}{team_name:<30}{home_avg:<18.2f}{away_avg:<18.2f}"
        f"{diff:<12.2f}"
    )
