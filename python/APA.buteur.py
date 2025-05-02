from fonction_commune_chahid import *

# Charger les données
match = lire_csv("data/Match.csv")
player = lire_csv("data/Player.csv") 
team =lire_csv("data/Team.csv")
match = match[(match["goal"].notna()) & (match["goal"] != "")]
goals_transformed = [transforme(g) for g in match["goal"]]
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
    d[e]=list(set(d[e]))
print(d) 

#But/tir cadre
#
