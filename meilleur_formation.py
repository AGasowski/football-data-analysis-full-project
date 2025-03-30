import pandas as pd

fichier_source = "Projet_info/data/Match.csv"
match = pd.read_csv(fichier_source)
match = match[match["season"] == "2015/2016"]
match=match[match["league_id"]==1729]
fichier_source2 = "Projet_info/data/Player.csv"
player = pd.read_csv(fichier_source2)
#match["home_player_Y1"]=match["home_player_Y1"].astype(int)
#player["player_api_id"]=player["player_api_id"].astype(int)
Away=[]
Away.append(match['away_player_Y2'].tolist())
Away.append(match['away_player_Y3'].tolist())
Away.append(match['away_player_Y4'].tolist())
Away.append(match['away_player_Y5'].tolist())
Away.append(match['away_player_Y6'].tolist())
Away.append(match['away_player_Y7'].tolist())
Away.append(match['away_player_Y8'].tolist())
Away.append(match['away_player_Y9'].tolist())
Away.append(match['away_player_Y10'].tolist())
Away.append(match['away_player_Y11'].tolist())
Home=[]
Home.append(match['home_player_Y2'].tolist())
Home.append(match['home_player_Y3'].tolist())
Home.append(match['home_player_Y4'].tolist())
Home.append(match['home_player_Y5'].tolist())
Home.append(match['home_player_Y6'].tolist())
Home.append(match['home_player_Y7'].tolist())
Home.append(match['home_player_Y8'].tolist())
Home.append(match['home_player_Y9'].tolist())
Home.append(match['home_player_Y10'].tolist())
Home.append(match['home_player_Y11'].tolist())
home_goal=match['home_team_goal'].tolist()
away_goal=match['away_team_goal'].tolist()


#print(Away[0])

def formation(L,h):
  assert h<=len(L[0])
  formation1=[]
  C=L[0][h]
  j=0
  for i in range(len(L)):
    if L[i][h]!=C:
        formation1.append(j)
        j=1
        C=L[i][h]
    else:
        j=j+1
  formation1.append(j) 
  return formation1 
d={}
for i in range(len(home_goal)): #la fonction tuple transforme une liste en tuple 
   if home_goal[i]>away_goal[i]:
      if tuple(formation(Home,i)) not in d:
         d[tuple(formation(Home,i))]=1
      else:
         d[tuple(formation(Home,i))]+=1
   if away_goal[i]>home_goal[i]:
       if tuple(formation(Away,i)) not in d:
         d[tuple(formation(Away,i))]=1
       else:
         d[tuple(formation(Away,i))]+=1
def max(d1):
   n=0
   cpt=0
   for e in d1:
      if d1[e]>=cpt:
         cpt=d[e]
         n=e

   return n

print(max(d)) 
    