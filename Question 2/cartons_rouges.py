import pandas as pd
import xml.etree.ElementTree as ET

# on importe la table match
fichier_source1 = "Projet_info/data/Match.csv"
match = pd.read_csv(fichier_source1)

# On importe la table player
fichier_source2 = "Projet_info/data/Player.csv"
player = pd.read_csv(fichier_source2)
player3 = pd.read_csv(fichier_source2)


match = match[match["season"] == "2015/2016"]
card1 = match[match["card"].notna() & (match["card"] != "")]


# On va créer une fonction qui prend en entré un fichier XML et qui la ressort
# en une table exploitable par python
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


C = []
for X in card1["card"]:
    C.append(transforme(X))

g = {}
for X in C:

    if "player1" in X.columns:
        player = X["player1"].tolist()
        card = X["card_type"].tolist()
        for i in range(len(player)):
            if card[i] == "r":
                if player[i] not in g:
                    g[player[i]] = 1
                else:
                    g[player[i]] += 1


player3["player_api_id"] = player3["player_api_id"].astype(str)
d3 = dict(zip(player3["player_name"], player3["player_api_id"]))
carton_rouges = {
    name: g.get(id) for name, id in d3.items() if g.get(id) is not None
}
meilleur_carton_rouges = sorted(
    carton_rouges.items(), key=lambda x: x[1], reverse=True
)[:30]
Classement_meilleurs_rouges = pd.DataFrame(
    meilleur_carton_rouges, columns=["player_name", "nb_carton jaune"]
)
print(Classement_meilleurs_rouges)
