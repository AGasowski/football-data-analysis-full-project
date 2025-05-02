"""
Script pour identifier les 10 meilleurs buteurs d'une saison donnée,
à partir des données de matchs et de joueurs.
"""

from project.src.fonctions.data_loader import charger_csv, transforme
from project.src.fonctions.statistiques import (
    compter_actions_par_joueur,
    trier_joueurs_par_actions,
)


def run_q4c(saison):
    """
    Affiche les 10 meilleurs buteurs pour une saison donnée.

    Args:
        saison (str): Saison ciblée, ex. "2014/2015"
    """
    print("== Résolution de la question 4 ==")

    # Charger les données
    match = charger_csv("data/Match.csv")
    player = charger_csv("data/Player.csv")

    # Filtrer le championnat et la saison souhaités
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == saison]
    # match = match[match["country_id"] == "1729"]  # facultatif si tu veux
    # filtrer par championnat

    # Transformer les colonnes goal en DataFrames
    goals_transformed = [transforme(g) for g in match["goal"]]

    # Compter les buts par joueur (player1)
    buts_par_joueur = compter_actions_par_joueur(goals_transformed, "player1")

    # Obtenir le top 10 des buteurs
    top_buteurs = trier_joueurs_par_actions(buts_par_joueur, player, top_n=10)

    # Afficher le classement
    print(top_buteurs)
