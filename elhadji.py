import pandas as pd
import xml.etree.ElementTree as ET

# Classement des meilleurs buteurs dans toute l'europe ( allez disons qu'on va
# faire le top 30 des meilleus buteurs ) tous championnats confondus : on aura
# donc besoin des tables match et player

# on importe la table match
fichier_source1 = "data/Match.csv"
match = pd.read_csv(fichier_source1)

# On importe la table player
fichier_source2 = "data/Player.csv"
player = pd.read_csv(fichier_source2)
player1 = pd.read_csv(fichier_source2)
player2 = pd.read_csv(fichier_source2)
player3 = pd.read_csv(fichier_source2)

# On commence d'abord a faire un classement pour la saison 2008/2009 pour la
# bundesliga

# Reduisons tout de méme la table match pour garder que les match de bundesliga
# En regardant la table league , on voit que le country id de la bundesliga
# vaut 7809 et donc on peut maintenant restreindre :


match = match[match["goal"].notna() & (match["goal"] != "")]
# match=match[match["country_id"] == "1729"]
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


# la colonne goal dans la table match a des elements qui sont eux meme des
# tables donc on va les stocker dans une liste L
L = []
for X in match["goal"]:
    L.append(transforme(X))


# Ainsi chaque element de la liste L correpond aux buts marqués pour un match
# de bundesliga . Donc l'idée ici est de créer un dictionnaire donc les clés
# seront les id des joueurs ayant marqués Et pour chaque clé , sa valeur sera
# le nombre de but marqué .

"""
for X in L:
    if "player1" not in X.columns :
      print("player1" in X.columns)  # Vérifier que la colonne est bien là
      print(X)
"""


d = {}
f = {}
for X in L:
    if "player1" in X.columns:
        player = X["player1"].tolist()

        # On parcourt les elements de la liste L , qui sont des tables de
        # matchs
        for i in range(len(player)):

            if player[i] not in d:
                d[player[i]] = 1
            else:
                # si le joueur est deja dans le dictionnaire , il avait donc
                # deja marqué et on ajoute alors de 1 son nb de but
                d[player[i]] += 1


player1["player_api_id"] = player1["player_api_id"].astype(str)
d1 = dict(zip(player1["player_name"], player1["player_api_id"]))
meilleurs_buteurs = {
    name: d.get(id) for name, id in d1.items() if d.get(id) is not None
}
meilleurs_buteurs = sorted(
    meilleurs_buteurs.items(), key=lambda x: x[1], reverse=True
)[:30]
Classement_meilleurs_buteurs = pd.DataFrame(
    meilleurs_buteurs, columns=["player_name", "nb_buts"]
)
print(Classement_meilleurs_buteurs)

# Classement meilleur passeur
for X in L:
    if "player2" in X.columns:
        player2 = X["player2"].tolist()

        # On parcourt les elements de la liste L , qui sont des tables de
        # matchs
        for i in range(len(player2)):

            if player2[i] not in f:
                f[player2[i]] = 1
            else:
                # si le joueur est deja dans le dictionnaire , il avait donc
                # deja marqué et on ajoute alors de 1 son nb de passe
                f[player2[i]] += 1


player3["player_api_id"] = player3["player_api_id"].astype(str)
d2 = dict(zip(player3["player_name"], player3["player_api_id"]))
meilleurs_passeurs = {
    name: f.get(id) for name, id in d2.items() if f.get(id) is not None
}
print(meilleurs_passeurs)
meilleurs_passeurs = sorted(
    meilleurs_passeurs.items(), key=lambda x: x[1], reverse=True
)[:30]
Classement_meilleurs_passeurs = pd.DataFrame(
    meilleurs_passeurs, columns=["player_name", "nb_passes"]
)
print(Classement_meilleurs_passeurs)
print(Classement_meilleurs_buteurs)


# classement carton jaunes

C = []
for X in card1["card"]:
    C.append(transforme(X))

g = {}
for X in C:

    if "player1" in X.columns:
        player = X["player1"].tolist()
        card = X["card_type"].tolist()

        # On parcourt les elements de la liste L , qui sont des tables de
        # matchs
        for i in range(len(player)):
            if card[i] == "y":
                if player[i] not in g:
                    g[player[i]] = 1
                else:
                    # si le joueur est deja dans le dictionnaire , il avait
                    # donc deja marqué et on ajoute alors de 1 son nb de but
                    g[player[i]] += 1


player3["player_api_id"] = player3["player_api_id"].astype(str)
d3 = dict(zip(player3["player_name"], player3["player_api_id"]))
carton_jaunes = {
    name: g.get(id) for name, id in d3.items() if g.get(id) is not None
}
meilleur_carton_jaune = sorted(
    carton_jaunes.items(), key=lambda x: x[1], reverse=True
)[:30]
Classement_meilleurs_jaunes = pd.DataFrame(
    meilleur_carton_jaune, columns=["player_name", "nb_carton jaune"]
)
print(Classement_meilleurs_jaunes)


"""
#Donc la le dictionnaire a les gens qui ont marqués et leurs nombres de buts on
va ainsi faire le lien avec la table player pour avoir le lien avec le nom des
joueurs ( bien sur que le classement viendra apres ) # Je m'interesse a la
table player et je vais garder que les colonnes : player_api_id et player_name
player=player[["player_api_id","player_name"]] #Ainsi je veux que les joueurs
qui ont marqué dans ma table donc je dois utiliser mon dictionnaire player =
player[player["player_api_id"].isin(d())] # il reste juste a ajouter une
nouvelle colonne que l'on va appeler but , et on utilise les valeurs des
dictionnaire
"""
