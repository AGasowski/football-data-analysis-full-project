import pandas as pd

fichier_source1 = "Projet_info/data/Match.csv"
match = pd.read_csv(fichier_source1)

# On importe la table player
fichier_source2 = "Projet_info/data/Team.csv"
team = pd.read_csv(fichier_source2)

match=match[match["league_id"]==1729]
match=match[match["season"]=="2014/2015"]

home_id=match['home_team_api_id'].tolist()
away_id=match['away_team_api_id'].tolist()
home_goal=match['home_team_goal'].tolist()
away_goal=match['away_team_goal'].tolist()

d={}
for i in range(len(home_id)):
        d[home_id[i]]=[0,0]
for i in range(len(away_id)):
        if away_id[i] not in d:
                d[away_id[i]]=[0,0]
for i in range(len(home_id)):
        if home_goal[i] > away_goal[i]:
                d[home_id[i]][0]+=3 
                d[home_id[i]][1]+=home_goal[i]-away_goal[i]
                d[away_id[i]][1]+=away_goal[i]-home_goal[i]
        if away_goal[i] > home_goal[i]:
                d[away_id[i]][0]+=3
                d[away_id[i]][1]+=away_goal[i]-home_goal[i]
                d[home_id[i]][1]+=home_goal[i]-away_goal[i]
        if home_goal[i] == away_goal[i]:
                d[home_id[i]][0]+=1
                d[away_id[i]][0]+=1
d1={}
team_id=team['team_api_id'].tolist()
team_name=team['team_long_name'].tolist()

def liaison_table(A,B,e):
        for i in range(len(A)):
                if A[i]==e:
                        return B[i] 
for e in d:
        d1[liaison_table(team_id,team_name,e)] = d[e]
#print(d1) 
Classement = pd.DataFrame.from_dict(d1, orient="index", columns=["Points", "Différence de buts"])
Classement= Classement.sort_values(by=["Points", "Différence de buts"], ascending=[False, False])

print(Classement) 