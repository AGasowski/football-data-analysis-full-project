from fonction_commune_chahid import *

# on importe la table match
match = lire_csv("data/Match.csv")

# On importe la table player
player = lire_csv("data/Player.csv")
player1 = lire_csv("data/Player.csv")

match = match[match["goal"].notna() & (match["goal"] != "")]
# match=match[match["country_id"] == "1729"]
match = match[match["season"] == "2015/2016"]

goals_transformed = [transforme(goal_str) for goal_str in match["goal"]]

convertir_int(player, "player_api_id")
convertir_int(player, "height")


header_scorers = set()
for goal_df in goals_transformed:
    # Vérification que 'goal_df' est bien un DataFrame
    if isinstance(goal_df, pd.DataFrame):
        # Vérification des colonnes 'player1' et 'subtype'
        if "player1" in goal_df.columns and "subtype" in goal_df.columns:
            # Extraction des colonnes 'player1' et 'subtype'
            table_player1 = goal_df["player1"].tolist()
            subtype = goal_df["subtype"].tolist()

            # On parcourt les éléments pour trouver les buteurs de la tête
            for player_id, sub in zip(table_player1, subtype):
                if sub == "header":
                    header_scorers.add(int(player_id))


# Construction d'une liste des tailles des joueurs concernés
player_id_to_height = dict(zip(player["player_api_id"], player["height"]))
header_heights = [
    player_id_to_height[pid]
    for pid in header_scorers
    if pid in player_id_to_height and player_id_to_height[pid] is not None
]

print(moyenne(header_heights))


"""

d = {}
for Goal in L:
    if "player1" in X.columns and "subtype" in X.columns:
        table_player1 = Goal["player1"].tolist()
        subtype = Goal["subtype"].tolist()

        # On parcourt les elements de la liste L , qui sont des tables de
        # matchs
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
"""
