from project.src.fonctions_communes import (
    lire_csv,
    transforme,
    convertir_int,
    get_scorers_by_subtype,
    get_taille_joueurs,
    moyenne,
)


def run_q3():
    print("== Résolution de la question 3 ==")

    # On importe la table match
    match = lire_csv("data/Match.csv")

    # On importe la table player
    player = lire_csv("data/Player.csv")

    match = match[match["goal"].notna() & (match["goal"] != "")]
    # match=match[match["country_id"] == "1729"]
    match = match[match["season"] == "2015/2016"]

    goals_transformed = [transforme(goal_str) for goal_str in match["goal"]]

    convertir_int(player, "player_api_id")
    convertir_int(player, "height")

    header_scorers = get_scorers_by_subtype(goals_transformed, "header")

    header_heights = []
    for pid in header_scorers:
        if get_taille_joueurs(player, pid) is not None:
            header_heights.append(get_taille_joueurs(player, pid))

    print(moyenne(header_heights))
