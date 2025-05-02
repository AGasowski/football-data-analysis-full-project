"""
Module pour afficher le classement des équipes avec la plus grande différence
de buts marqués à l'extérieur vs domicile.

Ce module traite les données des matchs de football pour calculer et afficher
le classement des équipes en fonction de la différence de buts marqués à
domicile et à l'extérieur.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.manipulations import (
    creer_dict,
    filtre_dic,
    cles_dic,
    ratio_dic,
    name_team_dic,
    id_championnat,
)
from project.src.fonctions.statistiques import compter_buts_matchs
from project.src.fonctions.utils import (
    trier,
)


def run_q9(saison, championnat):
    """
    Affiche le classement des équipes avec la plus grande différence de buts
    marqués à l'extérieur vs domicile pour une saison et un championnat donnés.

    Args:
        saison (str): Saison ciblée
        championnat (str): Nom du championnat ciblé
    """
    print("== Résolution de la question 9 ==")

    team_names = charger_csv(
        "data/Team.csv", "dict", "team_api_id", ("team_long_name")
    )

    # Dictionnaires pour stocker les statistiques des buts {team_id:
    # [total_buts, nb_matchs]}
    goals_home = creer_dict(2)
    goals_away = creer_dict(2)

    # Lecture du fichier des matchs et filtrage pour l'année 2014
    matchs = charger_csv(
        "data/Match.csv",
        "dict",
        "id",
        "season",
        "home_team_api_id",
        "away_team_api_id",
        "home_team_goal",
        "away_team_goal",
        "league_id",
    )
    if saison != "0":
        matchs = filtre_dic(matchs, 0, saison)
    id_champ = id_championnat(championnat)
    if id_champ != 0:
        matchs = filtre_dic(matchs, 5, str(id_champ))

    compter_buts_matchs(matchs, goals_home, 1, 3)
    compter_buts_matchs(matchs, goals_away, 2, 4)

    # Calcul des moyennes et différences
    classement = []

    for team in cles_dic(goals_home):
        home_avg = ratio_dic(goals_home, team, 0, 1)
        away_avg = ratio_dic(goals_away, team, 0, 1)
        classement.append((team, home_avg, away_avg, away_avg - home_avg))

    # Classement des équipes par ordre décroissant de différence
    trier(classement, 3, "liste")

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
