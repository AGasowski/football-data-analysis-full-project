### Code de Chahid

## Classement des meilleurs buteurs, passeurs carton jaune, carton rouge

import pandas as pd

fichier_source = "data/Match.csv"
df = pd.read_csv(fichier_source)
df_selectionne = df[["id", "country_id", "league_id", "season", "match_api_id", "home_team_api_id", "away_team_api_id", "home_team_goal", "away_team_goal"]]
