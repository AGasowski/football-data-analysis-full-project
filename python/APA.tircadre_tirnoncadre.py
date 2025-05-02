
from fonction_commune_chahid import *

# Charger les données
match = lire_csv("data/Match.csv")
player = lire_csv("data/Player.csv") 
team =lire_csv("data/Team.csv")
match = match[(match["shoton"].notna()) & (match["shoton"] != "")]
match = match[(match["shotoff"].notna()) & (match["shotoff"] != "")]
match = match[(match["goal"].notna()) & (match["goal"] != "")]

goals_transformed = [transforme(g) for g in match["goal"]]
shots_transformed=[transforme(s) for s in match["shoton"]]
tnc=[transforme(s) for s in match["shotoff"]] 
d={}
for goal in (goals_transformed):
    if ("team" in goal.columns) and ("player1" in goal.columns):
        colonne_team = [g for g in goal["team"]]
        colonne_player1 = [g for g in goal["player1"]]
        for i in range(len(colonne_team)):
            if colonne_team[i]not in d:
                d[str(colonne_team[i])]=[]
            d[str(colonne_team[i])].append(colonne_player1[i])
for e in d:
    d[e]=len(d[e])
s={}
for shot in (shots_transformed):
    if ("team" in shot.columns) and ("player1" in shot.columns):
        colonne_team = [g for g in shot["team"]]
        colonne_player1 = [g for g in shot["player1"]]
        for i in range(len(colonne_team)):
            if colonne_team[i]not in s:
                s[str(colonne_team[i])]=[]
            s[str(colonne_team[i])].append(colonne_player1[i])
for e in s :
    s[e]=len(s[e])
t={}
for shot in (tnc):
    if ("team" in shot.columns) and ("player1" in shot.columns):
        colonne_team = [g for g in shot["team"]]
        colonne_player1 = [g for g in shot["player1"]]
        for i in range(len(colonne_team)):
            if colonne_team[i]not in t:
                t[str(colonne_team[i])]=[]
            t[str(colonne_team[i])].append(colonne_player1[i])
for e in t:
    t[e]=len(t[e])
for e in d:
    if (e in s) and (e in t):
        d[e]=(d[e]+s[e])/(d[e]+s[e]+t[e]) 
    else:
        d[e]=d[e]/d[e] 
print(d) 
