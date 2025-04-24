from fonctions_utiles_panda import (
    lire_csv,
    select_saison,
    diff_abs,
    max,
    select,
    fusionner,
)

match = lire_csv("data/Match.csv")
match = select_saison(match, "2014/2015")
team = lire_csv("data/Team.csv")

match["home_team_api_id"] = (
    match["home_team_api_id"]
    .map(team.set_index("team_api_id")["team_long_name"])
    .fillna(match["home_team_api_id"])
)

match["ecart"] = diff_abs(match, "home_team_goal", "away_team_goal")

max_ecart = max(match, "ecart")

score = select(
    match,
    "ecart",
    max_ecart,
    ["home_team_goal", "away_team_goal", "home_team_api_id"],
)

print(score)
