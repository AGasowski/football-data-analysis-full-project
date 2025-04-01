import pandas as pd

fichier_source = "data/Match.csv"
df = pd.read_csv(fichier_source)
teams = pd.read_csv("data/Team.csv")[["team_api_id", "team_long_name"]]


home_team = df["home_team_api_id"].tolist()
away_team = df["away_team_api_id"].tolist()

home_goal = df["home_team_goal"].tolist()
away_goal = df["away_team_goal"].tolist()

def occurence(L,a):
    c = 0
    for i in range(len(L)):
        if a == L[i]:
            c+=1
    return c

d = {}
for i in range(len(home_team)):
    d[home_team[i]] = 0
for i in range(len(away_team)):
    if away_team[i] not in d:
        d[away_team[i]] = 0

for e in d:
    for i in range(len(home_team)):
        if e == home_team[i]:
            d[e] += away_goal[i]/occurence(away_team + home_team, home_team[i])
        elif e == away_team[i]:
            d[e] += home_goal[i]/occurence(away_team + home_team, home_team[i])

print(d)


def minimum(dico):
    min = dico[home_team[0]]
    for i in dico:
        if dico[i] <= min:
            min = dico[i]
    for i in dico:
        if dico[i] == min:
            return i


print(minimum(d))

id_teams = teams["team_api_id"].tolist()
name_team = teams["team_long_name"].tolist()

d2={}
for i in range(len(id_teams)):
    d2[id_teams[i]] = name_team[i]

'''
nom_equipe = d2[8121]

print(f"L'équipe qui a encaissé le moins de buts est : {nom_equipe}")'''