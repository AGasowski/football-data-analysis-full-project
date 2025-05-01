from project.src.fonctions.data_loader import (
    charger_csv,
    convertir_colonne,
    fusionner_colonnes_en_listes,
)
from project.src.fonctions.manipulations import filtrer_df
from project.src.fonctions.statistiques import resume_colonne
from project.src.fonctions.utils import (
    formation,
)


def run_q5(saison):
    print("== Résolution de la question 5 ==")

    match = charger_csv("data/Match.csv")
    if saison != 0:
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
    match["ecart"] = resume_colonne(
        match, "home_team_goal", "away_team_goal", "diff_abs"
    )
    diff_but = convertir_colonne(match, "ecart", "list")

    d = {}
    for i in range(len(diff_but)):
        if diff_but[i] > 0:
            if tuple(formation(Coordonée_home_joueur[i])) not in d:
                d[tuple(formation(Coordonée_home_joueur[i]))] = 1
            else:
                d[tuple(formation(Coordonée_home_joueur[i]))] += 1
        if diff_but[i] < 0:
            if tuple(formation(Coordonée_away_joueur[i])) not in d:
                d[tuple(formation(Coordonée_away_joueur[i]))] = 1
            else:
                d[tuple(formation(Coordonée_away_joueur[i]))] += 1

    classement = sorted(d.items(), key=lambda item: item[1], reverse=True)
    for rang, (formation1, nb_occurrences) in enumerate(classement, start=1):
        print(f"{rang}.  {formation1} - {nb_occurrences} fois")
