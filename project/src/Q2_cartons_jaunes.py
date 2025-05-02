from project.src.fonctions.data_loader import charger_csv, transforme
from project.src.fonctions.statistiques import (
    compter_actions_par_joueur,
    trier_joueurs_par_actions,
)
from project.src.fonctions.utils import (
    filtre_cartons,
)


def run_q2a(saison):
    print("== Résolution de la question 2 ==")

    # Charger les données
    match = charger_csv("data/Match.csv")
    player = charger_csv("data/Player.csv")

    # Filtrer le championnat et la saison souhaités
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == saison]
    # match = match[match["country_id"] == "1729"]  # facultatif si tu veux
    # filtrer par championnat

    # Transformer les colonnes goal en DataFrames
    card = [transforme(g) for g in match["card"]]

    carton_jaune_dfs = filtre_cartons(card, "y")

    # Étape 2 : utiliser la fonction générique
    jaunes_par_joueur = compter_actions_par_joueur(carton_jaune_dfs, "player1")
    top_jaunes = trier_joueurs_par_actions(jaunes_par_joueur, player, 10)
    print(top_jaunes)
