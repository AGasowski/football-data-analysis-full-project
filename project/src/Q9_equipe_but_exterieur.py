from project.src.fonctions_communes import (
    lire_csv_en_dict,
    creer_dict,
    compter_buts_matchs,
    filtre_dic,
    cles_dic,
    ratio_dic,
    trier_liste_tuples,
    name_team_dic,
)


def run_q9(saison):
    print("== Résolution de la question 9 ==")

    team_names = lire_csv_en_dict(
        "data/Team.csv", "team_api_id", ("team_long_name")
    )

    # Dictionnaires pour stocker les statistiques des buts {team_id:
    # [total_buts, nb_matchs]}
    goals_home = creer_dict(2)
    goals_away = creer_dict(2)

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

    matchs = filtre_dic(matchs, 0, saison)

    compter_buts_matchs(matchs, goals_home, 1, 3)
    compter_buts_matchs(matchs, goals_away, 2, 4)

    # Calcul des moyennes et différences
    classement = []

    for team in cles_dic(goals_home):
        home_avg = ratio_dic(goals_home, team, 0, 1)
        away_avg = ratio_dic(goals_away, team, 0, 1)
        classement.append((team, home_avg, away_avg, away_avg - home_avg))

    # Classement des équipes par ordre décroissant de différence
    trier_liste_tuples(classement, 3)

    # Affichage des 10 meilleures équipes
    print(
        "Classement des équipes avec la plus grande différence de buts "
        "marqués à l'extérieur vs domicile:"
    )
    print("-" * 100)
    print(
        f"{'Rang':<5}{'Équipe':<30}{'Moy. Buts Dom.':<18}"
        f"{'Moy. Buts Ext.':<18}{'Différence':<12}"
    )
    print("-" * 100)

    for rank, (team_id, home_avg, away_avg, diff) in enumerate(
        classement[:10], start=1
    ):  # Top 10
        team_name = name_team_dic(team_names, team_id)  # Récupérer le nom
        print(
            f"{rank:<5}{team_name:<30}{home_avg:<18.2f}{away_avg:<18.2f}"
            f"{diff:<12.2f}"
        )
