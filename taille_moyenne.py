import pandas as pd
import xml.etree.ElementTree as ET

fichier_source1 = "data/Match.csv"
match = pd.read_csv(fichier_source1)


fichier_source2 = "data/Player.csv"
player = pd.read_csv(fichier_source2)
player1 = pd.read_csv(fichier_source2)


match = match[match["goal"].notna() & (match["goal"] != '')]
match = match[match["season"] == "2015/2016"]

def transforme(X):
    root = ET.fromstring(X)
    data = []
    for value in root.findall("value"):
        entry = {child.tag: child.text for child in value if child.tag != "stats"}  # Exclure stats pour l'instant
        stats = value.find("stats")  # Extraire les stats
        if stats is not None:
            entry.update({f"stats_{child.tag}": child.text for child in stats})
            data.append(entry)
    # Convertir en DataFrame
    df = pd.DataFrame(data)
    return df

L = []
for X in match["goal"]:
    L.append(transforme(X))

player["player_api_id"] = player["player_api_id"].astype(int)
player["height"] = player["height"].astype(int)
d = {}
for X in L:
   if "player1" in X.columns and "subtype" in X.columns:
      table_player1 = X['player1'].tolist()
      subtype = X['subtype'].tolist()
      for i in range(len(table_player1)):
         if subtype[i] == "header":
            if table_player1[i] not in d:
                d[table_player1[i]] = 0
id1 = player['player_api_id'].tolist()
height = player['height'].tolist()
M=[]
for e,fg in d.items():
    M.append(e)
M = [int(i) for i in M]
N=[]
for i in range(len(id1)):
    if id1[i] in M:
        N.append(height[i])
print(N)
T = 0
for i in range (len(N)):
    T += N[i]/len(N)
print(T)
