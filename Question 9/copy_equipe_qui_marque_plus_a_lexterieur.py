import csv
from fonctions_utiles_panda import lire_csv_en_dict, creer_dict


team_names = lire_csv_en_dict(
    "data/Team.csv", "team_api_id", ("team_long_name")
)

# Dictionnaires pour stocker les statistiques des buts
goals_home = creer_dict(2)
# {team_id: [total_buts_domicile, nb_matchs_domicile]}
goals_away = creer_dict(2)
# {team_id: [total_buts_exterieur, nb_matchs_exterieur]}

# Lecture du fichier des matchs et filtrage pour l'année 2014

matchs = lire_csv_en_dict(
    "data/Match.csv",
    "id",
    "season",
    "home_team_api_id",
    "away_team_api_id",
    "home_team_goal",
    "away_team_goal",
)

print(matchs)

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
