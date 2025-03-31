import pandas as pd

fichier_source = "data/Match.csv"
df = pd.read_csv(fichier_source)
teams = pd.read_csv("data/Team.csv")[["team_api_id", "team_long_name"]]


buts_encaissés_domicile = df.groupby("home_team_api_id")["away_team_goal"].sum()
buts_encaissés_extérieur = df.groupby("away_team_api_id")["home_team_goal"].sum()

buts_totaux_encaissés = buts_encaissés_domicile.add(buts_encaissés_extérieur, fill_value=0)

equipe_moins_buts = buts_totaux_encaissés.idxmin()

nom_equipe = teams.loc[teams["team_api_id"] == equipe_moins_buts, "team_long_name"].values[0]

print(f"L'équipe qui a encaissé le moins de buts est : {nom_equipe}")