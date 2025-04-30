from project.src.fonctions_communes import (
    lire_csv,
    select_all,
    diff_abs,
    max_col,
    select,
    id_en_nom,
    afficher,
)


def run_q4(saison):
    print("== Résolution de la question 4 ==")
    match = lire_csv("data/Match.csv")
    match = select_all(match, "season", saison)
    team = lire_csv("data/Team.csv")

    id_en_nom(match, team)

    match["ecart"] = diff_abs(match, "home_team_goal", "away_team_goal")

    afficher(
        select(
            match,
            "ecart",
            max_col(match, "ecart"),
            "home_team",
            "home_team_goal",
            "away_team_goal",
            "away_team",
        )
    )
