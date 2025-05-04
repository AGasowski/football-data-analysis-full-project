from fonction_commune_chahid import *
from APS import process_player_attributes,moyenne
import math
import pandas as pd
# Charger les données
A=process_player_attributes("data/Player_Attributes.csv")
valeurs_interdites_saison = ["2006/2007","2016/2017"]
A = A[~A["saison"].isin(valeurs_interdites_saison)] 
def f(saison,id):
    s=[g for g in A["saison"]]
    id1 =[g for g in A["player_api_id"]]
    n=[g for g in A["overall_rating"]]
    for i in range(len(s)):
        if not math.isnan(int(id)):
           if (s[i]==saison) and (int(id1[i])==int(id)):
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
        if ("team" in goal.columns) and ("player2" in goal.columns):
            colonne_team = [g for g in goal["team"]]
            colonne_player1 = [g for g in goal["player2"]]
            for i in range(len(colonne_team)):
                if colonne_team[i] not in d:
                    d[str(colonne_team[i])] = []
                d[str(colonne_team[i])].append(colonne_player1[i])
    
    for e in d:
        d[e]=list(set(d[e]))
    for e in d:
        d[e][:]  =pd.Series(d[e]).dropna().tolist()
    for e in d:
        for i in range(len(d[e])):
             d[e][i]=(f(season,d[e][i]))
    for e in d:
        d[e]=moyenne(d[e])
    #print(d)
    return d


A1 = exo("2008/2009")  # d doit être retourné par la fonction exo
d1 = pd.DataFrame(list(A1.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d1["saison"] = "2008/2009"
A2 = exo("2009/2010")  # d doit être retourné par la fonction exo
d2 = pd.DataFrame(list(A2.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d2["saison"] = "2009/2010"
A3 = exo("2010/2011")  # d doit être retourné par la fonction exo
d3 = pd.DataFrame(list(A3.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d3["saison"] = "2010/2011"
A4 = exo("2011/2012")  # d doit être retourné par la fonction exo
d4 = pd.DataFrame(list(A4.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d4["saison"] = "2011/2012"
A5 = exo("2012/2013")  # d doit être retourné par la fonction exo
d5 = pd.DataFrame(list(A5.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d5["saison"] = "2012/2013" 
A6= exo("2013/2014")  # d doit être retourné par la fonction exo
d6 = pd.DataFrame(list(A6.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d6["saison"] = "2013/2014"
A7 = exo("2014/2015")  # d doit être retourné par la fonction exo
d7 = pd.DataFrame(list(A7.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d7["saison"] = "2014/2015"
A8 = exo("2015/2016")  # d doit être retourné par la fonction exo
d8 = pd.DataFrame(list(A8.items()), columns=["team_api_id", "moyenne_attributs_passeur"])
d8["saison"] = "2015/2016"
#print(d1) 

attribut_passeur=pd.concat([d1,d2,d3,d4,d5,d6,d7,d8], ignore_index=True)
attribut_passeur.to_pickle('attribut_passeur.pkl')
