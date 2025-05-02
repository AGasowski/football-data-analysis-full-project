"""
Script pour identifier le match avec l'écart de buts le plus important dans une
saison donnée. Utilise les données de match et d'équipes pour afficher les
résultats de manière lisible.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.manipulations import filtrer_df, id_en_nom
from project.src.fonctions.statistiques import resume_colonne
from project.src.fonctions.utils import (
    afficher,
)


def run_q2(saison):
    """
    Affiche le match avec le plus grand écart de buts pour une saison donnée.

    Args:
        saison (str): Saison ciblée au format "2014/2015". Si "0", utilise
        toutes les saisons.
    """
    print("== Résolution de la question 2 ==")
    match = charger_csv("data/Match.csv")
    if saison != "0":
        match = filtrer_df(match, "season", saison)
    team = charger_csv("data/Team.csv")

    id_en_nom(match, team)

    match["ecart"] = resume_colonne(
        match, "home_team_goal", "away_team_goal", "diff_abs"
    )

    afficher(
        filtrer_df(
            match,
            "ecart",
            resume_colonne(match, "ecart", None, "max"),
            ["home_team", "home_team_goal", "away_team_goal", "away_team"],
        )
    )
