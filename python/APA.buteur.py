from fonction_commune_chahid import *
from APS import process_player_attributes

# Charger les données
A=process_player_attributes("data/Player_Attributes.csv")
valeurs_interdites_saison = ["2006/2007","2016/2017"]
A = A[~A["saison"].isin(valeurs_interdites_saison)]
def f(saison,id):
    s=[g for g in A["saison"]]
    id1 =[g for g in A["player_api_id"]]
    n=[g for g in A["overall_rating"]]
    for i in range(len(s)):
        if (s[i]==saison) and (id1[i]==id):
            return n[i] 
def exo(season):
    match = lire_csv("data/Match.csv")
    player = lire_csv("data/Player.csv")
    team = lire_csv("data/Team.csv")
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == season]
    goals_transformed = [transforme(g) for g in match["goal"]]

    d = {}

    for goal in goals_transformed:
        if ("team" in goal.columns) and ("player1" in goal.columns):
            colonne_team = [g for g in goal["team"]]
            colonne_player1 = [g for g in goal["player1"]]
            for i in range(len(colonne_team)):
                if colonne_team[i] not in d:
                    d[str(colonne_team[i])] = []
                d[str(colonne_team[i])].append(colonne_player1[i])
    for e in d:
        for i in range(len(d[e])):
            d[e][i]=f(season,d[e][i])
    print(d)
exo("2014/2015")

# But/tir cadre
#
