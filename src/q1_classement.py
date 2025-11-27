"""
Script pour générer le classement d'un championnat donné pour une saison
spécifique, en analysant les données de matchs à partir de fichiers CSV.
"""

from src.fonctions.data_loader import (
    charger_csv,
)
from src.fonctions.manipulations import (
    creer_dict,
    filtre_dic,
    name_team_dic,
    id_championnat,
)
from src.fonctions.statistiques import (
    saison_equipe,
)


def run_q1(saison, championnat):
    """
    Affiche le classement d'un championnat donné pour une saison spécifique.

    Args:
        saison (str): Saison sous forme de chaîne, ex. "2014/2015" championnat
        (str): Nom du championnat, ex. "England Premier League"
    """
    print("=" * 80)
    print(f"    Classement de {championnat} pour la saison {saison}")
    print("=" * 80)

    team_names = charger_csv(
        "data/Team.csv", "dict", "team_api_id", "team_long_name"
    )

    # Lecture du fichier des matchs
    matchs = charger_csv(
        "data/Match.csv",
        "dict",
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

    matchs = filtre_dic(matchs, 0, saison)
    champ = id_championnat(championnat)
    matchs = filtre_dic(matchs, 1, str(champ))

    stats = saison_equipe(matchs)

    # Calcul du classement : Pts, Diff. Buts, Buts marqués
    classement = sorted(
        stats.items(),
        key=lambda x: (x[1][0], x[1][1] - x[1][2], x[1][1]),  # Pts, DB, BM
        reverse=True,
    )

    # En-tête
    print(f"{'Rang':<5} {'Équipe':<30} {'Pts':<5} {'DB':<5} {'BM':<5}")

    # Affichage avec rang
    for i, (team_id, (points, scored, conceded)) in enumerate(
        classement, start=1
    ):
        nom = name_team_dic(team_names, team_id)
        db = scored - conceded
        print(f"{i:<5} {nom:<30} {points:<5} {db:<5} {scored:<5}")
