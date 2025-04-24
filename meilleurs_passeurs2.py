import pandas as pd
from fonctions_utiles_panda import transforme
from Fonction_utile import convertir_str

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

match = match[match["goal"].notna() & (match["goal"] != "")]
# match=match[match["country_id"] == "1729"]
match = match[match["season"] == "2015/2016"]
card1 = match[match["card"].notna() & (match["card"] != "")]

# la colonne goal dans la table match a des elements qui sont eux meme des
# tables donc on va les stocker dans une liste L
L = []
for X in match["goal"]:
    L.append(transforme(X))


# Ainsi chaque element de la liste L correpond aux buts marqués pour un match
# de bundesliga . Donc l'idée ici est de créer un dictionnaire donc les clés
# seront les id des joueurs ayant marqués Et pour chaque clé , sa valeur sera
# le nombre de but marqué .

# Classement meilleur passeur
f = {}
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


convertir_str(player3, "player_api_id")
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
