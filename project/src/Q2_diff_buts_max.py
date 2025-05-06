"""
Script pour identifier le match avec l'écart de buts le plus important dans une
saison donnée. Utilise les données de match et d'équipes pour afficher les
résultats de manière lisible.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.manipulations import (
    filtrer_df,
    id_en_nom,
    id_championnat,
)
from project.src.fonctions.statistiques import resume_colonne
from project.src.fonctions.utils import (
    afficher,
)


def run_q2(saison, championnat):
    """
    Affiche le match avec le plus grand écart de buts pour une saison donnée.

    Args:
        saison (str): Saison ciblée au format "2014/2015". Si "0", utilise
        toutes les saisons.
    """
    print("=" * 56)
    print(
        f"    Matchs avec la plus grande différence de buts"
        f"{f' ({saison})' if saison != '0' else ''}"
        f"{f' ({championnat})' if championnat != "Tous les championnats réunis"
           else ''}"
    )
    print("=" * 56)

    match = charger_csv("data/Match.csv")
    if saison != "0":
        match = filtrer_df(match, "season", saison)
    id_champ = id_championnat(championnat)
    if id_champ != 0:
        match = filtrer_df(match, "league_id", int(id_champ))
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
        ),
        False,
    )
