import pandas as pd
import xml.etree.ElementTree as ET

# Classement des meilleurs buteurs dans toute l'europe ( allez disons qu'on va faire le top 30 des meilleus buteurs )
# tous championnats confondus : on aura donc besoin des tables match et player

# on importe la table match
fichier_source1 = "data/Match.csv"
match = pd.read_csv(fichier_source1)

# On importe la table player
fichier_source2 = "data/Player.csv"
player = pd.read_csv(fichier_source2)
player1 = pd.read_csv(fichier_source2)


match = match[match["goal"].notna() & (match["goal"] != "")]
# match=match[match["country_id"] == "1729"]
match = match[match["season"] == "2015/2016"]

# On va créer une fonction qui prend en entré un fichier XML et qui la ressort en une table exploitable par python


def transforme(X):
    root = ET.fromstring(X)
    data = []
    for value in root.findall("value"):
        entry = {
            child.tag: child.text for child in value if child.tag != "stats"
        }  # Exclure stats pour l'instant
        stats = value.find("stats")  # Extraire les stats
        if stats is not None:
            entry.update({f"stats_{child.tag}": child.text for child in stats})
            data.append(entry)
    # Convertir en DataFrame
    df = pd.DataFrame(data)
    return df


# la colonne goal dans la table match a des elements qui sont eux meme des tables donc on va les stocker dans une liste L
L = []
for X in match["goal"]:
    L.append(transforme(X))


# Ainsi chaque element de la liste L correpond aux buts marqués pour un match de bundesliga .
# Donc l'idée ici est de créer un dictionnaire donc les clés seront les id des joueurs ayant marqués
# Et pour chaque clé , sa valeur sera le nombre de but marqué .

"""
for X in L:
    if "player1" not in X.columns :
      print("player1" in X.columns)  # Vérifier que la colonne est bien là
      print(X)
"""
player["player_api_id"] = player["player_api_id"].astype(int)
player["height"] = player["height"].astype(int)
"""
def taille( id1):
    id=player['player_api_id'].tolist()
    height = player['height'].tolist()
    for i in range(len(id)):
        if id1==id[i]:
            return height[i]
"""
d = {}


for X in L:
    if "player1" in X.columns and "subtype" in X.columns:
        table_player1 = X["player1"].tolist()
        subtype = X["subtype"].tolist()

        # On parcourt les elements de la liste L , qui sont des tables de matchs
        for i in range(len(table_player1)):
            if subtype[i] == "header":
                if table_player1[i] not in d:
                    d[table_player1[i]] = 0
id1 = player["player_api_id"].tolist()
height = player["height"].tolist()
M = []
for e, fg in d.items():
    M.append(e)
M = [int(i) for i in M]
N = []
for i in range(len(id1)):
    if id1[i] in M:
        N.append(height[i])
print(N)

T = 0
for i in range(len(N)):
    T += N[i] / len(N)

print(T)
