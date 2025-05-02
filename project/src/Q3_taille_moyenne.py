"""
Script pour analyser les buteurs sur coups de tête dans un championnat et une
saison donnés. Calcule la taille moyenne des joueurs ayant marqué de la tête.
"""

from project.src.fonctions.data_loader import (
    charger_csv,
    transforme,
    convertir_colonne,
)
from project.src.fonctions.statistiques import (
    get_scorers_by_subtype,
    calculer_moyenne,
)
from project.src.fonctions.utils import (
    get_taille_joueurs,
)
from project.src.fonctions.manipulations import id_championnat, filtrer_df


def run_q3(saison, championnat):
    """
    Calcule et affiche la taille moyenne des joueurs ayant marqué de la tête
    pour un championnat et une saison donnés.

    Args:
        saison (str): Saison ciblée, ex. "2014/2015". Si "0", toutes les
        saisons sont prises en compte.

        championnat (str): Nom du championnat ciblé.
    """
    print("== Résolution de la question 3 ==")

    # On importe la table match
    match = charger_csv("data/Match.csv")

    # On importe la table player
    player = charger_csv("data/Player.csv")

    match = match[match["goal"].notna() & (match["goal"] != "")]

    if saison != "0":
        match = filtrer_df(match, "season", saison)
    id_champ = id_championnat(championnat)
    if championnat != 0:
        match = filtrer_df(match, "league_id", int(id_champ))

    goals_transformed = [transforme(goal_str) for goal_str in match["goal"]]

    convertir_colonne(player, "player_api_id", "int")
    convertir_colonne(player, "height", "int")

    header_scorers = get_scorers_by_subtype(goals_transformed, "header")

    header_heights = []
    for pid in header_scorers:
        if get_taille_joueurs(player, pid) is not None:
            header_heights.append(get_taille_joueurs(player, pid))

    print(calculer_moyenne(header_heights))
