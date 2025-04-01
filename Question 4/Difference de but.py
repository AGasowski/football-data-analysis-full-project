import pandas as pd

fichier_source = "data/Match.csv"
match = pd.read_csv(fichier_source)
match = match[match["season"] == "2014/2015"]
data_team = "data/Team.csv"
team = pd.read_csv(data_team)

match["home_team_api_id"] = match["home_team_api_id"].astype(int)
match["away_team_api_id"] = match["away_team_api_id"].astype(int)
team["team_api_id"] = team["team_api_id"].astype(int)

home_goal = match["home_team_goal"].tolist()
away_goal = match["away_team_goal"].tolist()
home_team = match["home_team_api_id"].tolist()
away_team = match["away_team_api_id"].tolist()
team_name = team["team_long_name"].tolist()
team_id = team["team_api_id"].tolist()

L = []
for i in range(len(home_goal)):
    L.append(abs(home_goal[i] - away_goal[i]))


def max(M):
    cpt = 0
    for i in range(len(M)):
        if M[i] >= cpt:
            cpt = M[i]
    return cpt


a = max(L)


def liaison_table(A, B, i):
    for j in range(len(A)):
        if A[j] == i:
            return B[j]


for i in range(len(L)):
    if L[i] == a:
        print(
            liaison_table(team_id, team_name, home_team[i]),
            liaison_table(team_id, team_name, away_team[i]),
            home_goal[i],
            away_goal[i],
        )
