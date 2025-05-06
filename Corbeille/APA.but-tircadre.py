from fonction_commune_chahid import *

# Charger les données

def exo(season):
    match = lire_csv("data/Match.csv")
    player = lire_csv("data/Player.csv")
    team = lire_csv("data/Team.csv")
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[(match["shoton"].notna()) & (match["shoton"] != "")]
    match = match[match["season"] == season]    
    goals_transformed = [transforme(g) for g in match["goal"]]
    shots_transformed = [transforme(s) for s in match["shoton"]]
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
        d[e] = len(d[e])
    s = {}
    for shot in shots_transformed:
        if ("team" in shot.columns) and ("player1" in shot.columns):
            colonne_team = [g for g in shot["team"]]
            colonne_player1 = [g for g in shot["player1"]]
            for i in range(len(colonne_team)):
                if colonne_team[i] not in s:
                    s[str(colonne_team[i])] = []
                s[str(colonne_team[i])].append(colonne_player1[i])
    for e in s:
        s[e] = len(s[e])
    for e in d:
        if e in s:
            d[e] = d[e] / (d[e] + s[e])
        else:
            d[e]=d[e]/d[e] 
    #print(d) 
    return(d) 
A1 = exo("2008/2009")  # d doit être retourné par la fonction exo
d1 = pd.DataFrame(list(A1.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d1["saison"] = "2008/2009"
A2 = exo("2009/2010")  # d doit être retourné par la fonction exo
d2 = pd.DataFrame(list(A2.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d2["saison"] = "2009/2010"
A3 = exo("2010/2011")  # d doit être retourné par la fonction exo
d3 = pd.DataFrame(list(A3.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d3["saison"] = "2010/2011"
A4 = exo("2011/2012")  # d doit être retourné par la fonction exo
d4 = pd.DataFrame(list(A4.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d4["saison"] = "2011/2012"
A5 = exo("2012/2013")  # d doit être retourné par la fonction exo
d5 = pd.DataFrame(list(A5.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d5["saison"] = "2012/2013" 
A6= exo("2013/2014")  # d doit être retourné par la fonction exo
d6 = pd.DataFrame(list(A6.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d6["saison"] = "2013/2014"
A7 = exo("2014/2015")  # d doit être retourné par la fonction exo
d7 = pd.DataFrame(list(A7.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d7["saison"] = "2014/2015"
A8 = exo("2015/2016")  # d doit être retourné par la fonction exo
d8 = pd.DataFrame(list(A8.items()), columns=["team_api_id", "ratio_but_tir_cadre"])
d8["saison"] = "2015/2016"

but_tircadre=pd.concat([d1,d2,d3,d4,d5,d6,d7,d8], ignore_index=True)
but_tircadre.to_pickle('but_tircadre.pkl')