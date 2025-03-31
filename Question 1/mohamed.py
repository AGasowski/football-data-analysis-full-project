import pandas as pd

fichier_source = "data/Match.csv"
df = pd.read_csv(fichier_source)
#teams = pd.read_csv("data/Team.csv")[["team_api_id", "team_long_name"]]
home_team=df['home_team_api_id'].tolist()
away_team=df['away_team_api_id'].tolist()

home_goal = df['home_team_goal'].tolist()
away_goal = df['away_team_goal'].tolist()

d={}
for i in range(len(home_team)):
    d[home_team[i]]=0
for i in range(len(away_team)):
    if away_team[i] not in d:
        d[away_team[i]]=0

for e in d:
    for i in range(len(home_team)):
        if e == home_team[i] :
            d[e] += away_goal[i]
        elif e== away_team[i]:
            d[e] += home_goal[i]

print(d)

def minimum(dico):
    min=dico[home_team[0]]
    for i in dico:
        if dico[i] <= min:
            min = dico[i]
    for i in dico:
        if dico[i]==min:
            return i 

print(minimum(d))





'''

buts_encaissés_domicile = df.groupby("home_team_api_id")["away_team_goal"].sum()
buts_encaissés_extérieur = df.groupby("away_team_api_id")["home_team_goal"].sum()

buts_totaux_encaissés = buts_encaissés_domicile.add(buts_encaissés_extérieur, fill_value=0)

equipe_moins_buts = buts_totaux_encaissés.idxmin()

nom_equipe = teams.loc[teams["team_api_id"] == equipe_moins_buts, "team_long_name"].values[0]]

print(f"L'équipe qui a encaissé le moins de buts est : {nom_equipe}")