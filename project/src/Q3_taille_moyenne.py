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


def run_q3():
    print("== Résolution de la question 3 ==")

    # On importe la table match
    match = charger_csv("data/Match.csv")

    # On importe la table player
    player = charger_csv("data/Player.csv")

    match = match[match["goal"].notna() & (match["goal"] != "")]
    # match=match[match["country_id"] == "1729"]
    match = match[match["season"] == "2015/2016"]

    goals_transformed = [transforme(goal_str) for goal_str in match["goal"]]

    convertir_colonne(player, "player_api_id", "int")
    convertir_colonne(player, "height", "int")

    header_scorers = get_scorers_by_subtype(goals_transformed, "header")

    header_heights = []
    for pid in header_scorers:
        if get_taille_joueurs(player, pid) is not None:
            header_heights.append(get_taille_joueurs(player, pid))

    print(calculer_moyenne(header_heights))
