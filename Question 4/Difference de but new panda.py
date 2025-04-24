from fonctions_utiles_panda import (
    lire_csv,
    select_saison,
    diff_abs,
    max,
    select,
    id_en_nom,
    afficher,
)

match = lire_csv("data/Match.csv")
match = select_saison(match, "2014/2015")
team = lire_csv("data/Team.csv")

id_en_nom(match, team)

match["ecart"] = diff_abs(match, "home_team_goal", "away_team_goal")

scores = select(
    match,
    "ecart",
    max(match, "ecart"),
    [
        "home_team",
        "home_team_goal",
        "away_team_goal",
        "away_team",
    ],
)

afficher(scores)
