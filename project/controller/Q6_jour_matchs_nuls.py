from project.controller.fonctions_communes import (
    lire_csv,
    convertir_date,
    select_all,
    nb_occurences,
    max_serie,
    date_format,
)


def run_q6():
    print("== Résolution de la question 6 ==")

    # Charger les données
    match = lire_csv("data/Match.csv")

    # Modifier la colonne 'date' en format datetime et en français
    convertir_date(match)

    # Filtrer les matchs nuls
    matchs_nuls = select_all(match, "home_team_goal", match["away_team_goal"])

    # Trouver le jour avec le plus de matchs nuls
    jour_max, nb_max = max_serie(nb_occurences(matchs_nuls, "date"))

    print(
        f"Le jour qui a connu le plus de matchs nuls est le "
        f"{date_format(jour_max)} avec {nb_max} matchs nuls."
    )
