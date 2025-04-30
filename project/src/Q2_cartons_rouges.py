from project.src.fonctions_communes import (
    lire_csv,
    transforme,
    compter_actions_par_joueur,
    trier_joueurs_par_actions,
    filtre_cartons,
)


def run_q2b(saison):
    print("== Résolution de la question 2 ==")

    # Charger les données
    match = lire_csv("data/Match.csv")
    player = lire_csv("data/Player.csv")

    # Filtrer le championnat et la saison souhaités
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == saison]
    # match = match[match["country_id"] == "1729"]  # facultatif si tu veux
    # filtrer par championnat

    # Transformer les colonnes goal en DataFrames
    card = [transforme(g) for g in match["card"]]

    carton_rouge_dfs = filtre_cartons(card, "r")

    # Étape 2 : utiliser la fonction générique
    rouges_par_joueur = compter_actions_par_joueur(carton_rouge_dfs, "player1")
    top_rouges = trier_joueurs_par_actions(rouges_par_joueur, player, top_n=10)
    print(top_rouges)
