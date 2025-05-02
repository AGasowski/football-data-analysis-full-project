"""
Module pour analyser les jours où il y a eu le plus de matchs nuls.

Ce script transforme les dates en format lisible, filtre les matchs nuls, puis
identifie le jour ayant connu le plus de matchs nuls parmi tous les matchs
enregistrés.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.dates_formats import convertir_date, date_format
from project.src.fonctions.manipulations import filtrer_df
from project.src.fonctions.statistiques import (
    nb_occurences,
    max_serie,
)


def run_q6():
    """
    Affiche le jour où il y a eu le plus de matchs nuls.

    Étapes : - Chargement et conversion des dates des matchs - Filtrage des
    matchs nuls (égalité des scores) - Calcul du jour avec le plus
    d’occurrences de matchs nuls
    """
    print("== Résolution de la question 6 ==")

    # Charger les données
    match = charger_csv("data/Match.csv")

    # Modifier la colonne 'date' en format datetime et en français
    convertir_date(match)

    # Filtrer les matchs nuls
    matchs_nuls = filtrer_df(match, "home_team_goal", match["away_team_goal"])

    # Trouver le jour avec le plus de matchs nuls
    jour_max, nb_max = max_serie(nb_occurences(matchs_nuls, "date"))

    print(
        f"Le jour qui a connu le plus de matchs nuls est le "
        f"{date_format(jour_max)} avec {nb_max} matchs nuls."
    )
