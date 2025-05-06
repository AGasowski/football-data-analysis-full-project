"""
Script pour analyser les jours où il y a eu le plus de matchs nuls.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.dates_formats import convertir_date, date_format
from project.src.fonctions.manipulations import filtrer_df, get_saison
from project.src.fonctions.statistiques import (
    nb_occurences,
    max_serie,
)


def run_q6(saison):
    """
    Affiche le jour où il y a eu le plus de matchs nuls.

    Args:
        saison (str): Saison sous forme de chaîne, ex. "2014/2015"
    """
    print("==================================================================")
    print(
        f"         Jour qui a connu le plus de matchs nuls"
        f"{f' ({saison})' if saison != '0' else ''}"
    )
    print("==================================================================")

    # Charger les données
    match = charger_csv("data/Match.csv")

    # Modifier la colonne 'date' en format datetime et en français
    convertir_date(match)

    match = convertir_date(match)

    if saison != "0":
        match = get_saison(match)
        match = filtrer_df(match, "saison", saison)

    # Filtrer les matchs nuls
    matchs_nuls = filtrer_df(match, "home_team_goal", match["away_team_goal"])

    # Trouver le jour avec le plus de matchs nuls
    jour_max, nb_max = max_serie(nb_occurences(matchs_nuls, "date"))

    print("Le jour qui a connu le plus de matchs nuls est le ")
    print(f"{date_format(jour_max)} avec {nb_max} matchs nuls.")
