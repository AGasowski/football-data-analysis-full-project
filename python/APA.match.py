import pandas as pd

# Exemple : tes DataFrames
team_stats = pd.read_pickle("enfin.pkl")
matches = pd.read_csv("data/Match.csv")
matches = matches.rename(columns={"season": "saison"})


# On crée un ensemble de tuples (season, team_id) valides dans team_stats
valid_teams = set(zip(team_stats["saison"], team_stats["team_api_id"]))


# Fonction pour tester si une ligne du match est valide (home et away présents dans team_stats)
def match_is_valid(row):
    return (row["saison"], row["home_team_api_id"]) in valid_teams and (
        row["saison"],
        row["away_team_api_id"],
    ) in valid_teams


# On applique ce filtre
matches_filtered = matches[matches.apply(match_is_valid, axis=1)]
match = matches_filtered[
    [
        "league_id",
        "date" "saison",
        "home_team_api_id",
        "away_team_api_id",
        "home_team_goal",
        "away_team_goal",
    ]
]
match.to_excel("match2.xlsx")
match.to_csv("match.csv")
