from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.manipulations import filtrer_df, id_en_nom
from project.src.fonctions.statistiques import resume_colonne
from project.src.fonctions.utils import (
    afficher,
)


def run_q4(saison):
    print("== Résolution de la question 4 ==")
    match = charger_csv("data/Match.csv")
    if saison != 0:
        match = filtrer_df(match, "season", saison)
    team = charger_csv("data/Team.csv")

    id_en_nom(match, team)

    match["ecart"] = resume_colonne(
        match, "home_team_goal", "away_team_goal", "diff_abs"
    )

    afficher(
        filtrer_df(
            match,
            "ecart",
            resume_colonne(match, "ecart", None, "max"),
            ["home_team", "home_team_goal", "away_team_goal", "away_team"],
        )
    )
