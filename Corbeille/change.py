import pandas as pd

team = pd.read_csv("data/Team.csv")
id_team = [g for g in team["team_api_id"]]
nom_team = [g for g in team["team_long_name"]]


def id_to_nom(id):
    for i in range(len(id_team)):
        if id_team[i] == id:
            return nom_team[i]
