"""
Script pour générer le classement des dispositifs les plus utilisés pour une
saison spécifique, en analysant les données de matchs à partir de fichiers CSV.
"""

from project.src.fonctions.data_loader import (
    charger_csv,
    fusionner_colonnes_en_listes,
)
from project.src.fonctions.manipulations import filtrer_df
from project.src.fonctions.utils import formation, trier


def run_q5(saison):
    """
    Affiche le classement des dispositifs pour une saison spécifique.

    Args:
        saison (str): Saison sous forme de chaîne, ex. "2014/2015"
    """
    print("==================================================================")
    print(f"    Classement des dispositifs les plus utilisés ({saison})")
    print("==================================================================")

    match = charger_csv("data/Match.csv")
    if saison != "0":
        match = filtrer_df(match, "season", saison)
    match = filtrer_df(match, "league_id", 21518)

    Coordonée_home_joueur = fusionner_colonnes_en_listes(
        match,
        [
            "home_player_Y2",
            "home_player_Y3",
            "home_player_Y4",
            "home_player_Y5",
            "home_player_Y6",
            "home_player_Y7",
            "home_player_Y8",
            "home_player_Y9",
            "home_player_Y10",
            "home_player_Y11",
        ],
    )
    Coordonée_away_joueur = fusionner_colonnes_en_listes(
        match,
        [
            "away_player_Y2",
            "away_player_Y3",
            "away_player_Y4",
            "away_player_Y5",
            "away_player_Y6",
            "away_player_Y7",
            "away_player_Y8",
            "away_player_Y9",
            "away_player_Y10",
            "away_player_Y11",
        ],
    )

    d = {}
    for i in range(len(Coordonée_home_joueur)):
        if tuple(formation(Coordonée_home_joueur[i])) not in d:
            d[tuple(formation(Coordonée_home_joueur[i]))] = 1
        else:
            d[tuple(formation(Coordonée_home_joueur[i]))] += 1
        if tuple(formation(Coordonée_away_joueur[i])) not in d:
            d[tuple(formation(Coordonée_away_joueur[i]))] = 1
        else:
            d[tuple(formation(Coordonée_away_joueur[i]))] += 1

    classement = trier(d, par=1, type_data="dict", reverse=True)

    for rank, (formation1, nb_occurrences) in enumerate(
        classement.items(), start=1
    ):
        formation1 = " ".join(str(x) for x in formation1)
        print(f"{rank:<5}{formation1:<20}{nb_occurrences} fois")
