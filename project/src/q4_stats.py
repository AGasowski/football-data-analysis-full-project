"""
Script pour identifier les 10 joueurs ayant reçu le plus de cartons jaunes
durant une saison donnée, en analysant les données de matchs.
"""

from project.src.fonctions.data_loader import charger_csv, transforme
from project.src.fonctions.statistiques import (
    compter_actions_par_joueur,
    trier_joueurs_par_actions,
)
from project.src.fonctions.utils import (
    filtre_cartons,
)
from project.src.fonctions.manipulations import id_championnat, filtrer_df


def run_q4(saison, championnat, type_action):
    """
    Affiche les 10 joueurs ayant reçu le plus de cartons jaunes pour une saison
    donnée.

    Args:
        saison (str): Saison ciblée, ex. "2014/2015"
    """
    couleur = ""
    joueur = ""
    nom = ""
    titre = ""
    # Type de classement
    if type_action == "jaune":
        type_action = "card"
        couleur = "y"
        joueur = "player1"
        nom = "Nombre de cartons jaunes"
        titre = "cartons jaunes"
    if type_action == "rouge":
        type_action = "card"
        joueur = "player1"
        couleur = "r"
        nom = "Nombre de cartons rouges"
        titre = "cartons rouges"
    if type_action == "but":
        type_action = "goal"
        joueur = "player1"
        nom = "Nombre de buts"
        titre = "meilleurs buteurs"
    if type_action == "passe":
        type_action = "goal"
        joueur = "player2"
        nom = "Nombre de passes décisives"
        titre = "meilleurs passeurs"

    print("==================================================================")
    print(f"    Classement des {titre} pour la saison {saison}")
    print(
        f"    {f' {championnat}' if championnat != 'Tous les championnats '
               'réunis'
               else ''}"
    )
    print("==================================================================")

    # Charger les données
    match = charger_csv("data/Match.csv")
    player = charger_csv("data/Player.csv")

    # Filtrer le championnat et la saison souhaités
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == saison]
    id_champ = id_championnat(championnat)
    if id_champ != 0:
        match = filtrer_df(match, "league_id", int(id_champ))

    # Transformer les colonnes goal en DataFrames
    carton_but = [transforme(g) for g in match[type_action]]

    if type_action == "card":
        carton_but = filtre_cartons(carton_but, couleur)

    # Étape 2 : utiliser la fonction générique
    compte_par_joueur = compter_actions_par_joueur(carton_but, joueur)
    top = trier_joueurs_par_actions(compte_par_joueur, player, nom, 10)
    print(top)
