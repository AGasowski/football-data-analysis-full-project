from fonctions_communes import (
    lire_csv_en_dict,
    creer_dict,
    filtre_dic,
    saison_equipe,
    name_team_dic,
)


def run_q1():
    print("== Résolution de la question 1 ==")

    team_names = lire_csv_en_dict(
        "data/Team.csv", "team_api_id", ("team_long_name")
    )

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

    stats = saison_equipe(matchs)

    classement = sorted(stats.items(), key=lambda x: x[1][0], reverse=True)

    # En-tête
    print(f"{'Équipe':<30} {'Pts':<5} {'BM':<5} {'BE':<5}")

    # Affichage
    for team_id, (points, scored, conceded) in classement:
        nom = name_team_dic(team_names, team_id)
        print(f"{nom:<30} {points:<5} {scored:<5} {conceded:<5}")
