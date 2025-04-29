import pandas as pd

# Charger les données
team_attributes = pd.read_csv("data/Team_Attributes.csv")
teams = pd.read_csv("data/Team.csv")[["team_api_id", "team_long_name"]]

# Vérifier les valeurs uniques de buildUpPlaySpeedClass
print(team_attributes["buildUpPlaySpeedClass"].unique())

# Sélectionner les équipes avec un style de jeu "Fast" en attaque
best_teams = team_attributes[team_attributes["buildUpPlaySpeedClass"] == "Fast"]

# Associer les noms des équipes
best_teams = best_teams.merge(teams, on="team_api_id", how="left")

# Afficher les équipes
print(best_teams[["team_long_name", "buildUpPlaySpeedClass", "buildUpPlayPassingClass"]])
