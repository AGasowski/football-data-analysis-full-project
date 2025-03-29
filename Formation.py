#on determine la formation avec le plus de victoire
import pandas as pd

fichier_source = "Projet_info/data/Match.csv"
match = pd.read_csv(fichier_source)
match = match[match["season"] == "2015/2016"]
match=match[match["league_id"]==1729]
fichier_source2 = "Projet_info/data/Player.csv"
player = pd.read_csv(fichier_source2)
#match["home_player_Y1"]=match["home_player_Y1"].astype(int)
#player["player_api_id"]=player["player_api_id"].astype(int)
A=[]
A.append(match['away_player_Y2'].tolist())
A.append(match['away_player_Y3'].tolist())
A.append(match['away_player_Y4'].tolist())
A.append(match['away_player_Y5'].tolist())
A.append(match['away_player_Y6'].tolist())
A.append(match['away_player_Y7'].tolist())
A.append(match['away_player_Y8'].tolist())
A.append(match['away_player_Y9'].tolist())
A.append(match['away_player_Y10'].tolist())
A.append(match['away_player_Y11'].tolist())


#print(M)

ensemble=[]
for h in range(len(A[0])):
 formation=[]
 C=A[0][h]
 j=0
 for i in range(len(A)):
    if A[i][h]!=C:
        formation.append(j)
        j=1
        C=A[i][h]
    else:
        j=j+1
 formation.append(j) 
 ensemble.append(formation)
 print(ensemble)
 



