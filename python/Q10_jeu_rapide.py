import pandas as pd
import matplotlib.pyplot as plt
from fonctions_communes import *


def convertir_colonne_en_datetime(df, colonne):
    df[colonne] = pd.to_datetime(df[colonne])
    return df


def creer_colonne_age_au_moment(df, colonne_anniv, colonne_eval):
    df["age"] = (df[colonne_eval] - df[colonne_anniv]).dt.days // 365
    return df


def creer_tranche_age(df, col_age):
    bins = [0, 22, 27, 32, 37, 100]
    labels = ["18-22", "23-27", "28-32", "33-37", "38+"]
    df["age_group"] = pd.cut(
        df[col_age], bins=bins, labels=labels, right=False
    )
    return df


# Charger les données
player_attributes = lire_csv("data/Player_Attributes.csv")
players = lire_csv("data/Player.csv")

# Fusionner les tables pour avoir la date de naissance
player_data = fusionner(
    player_attributes, players, "player_api_id", "player_api_id"
)

# Convertir les dates
player_data = convertir_date(player_data)  # convertit la colonne 'date'
player_data = convertir_colonne_en_datetime(
    player_data, "birthday"
)  # convertit 'birthday'

# Calculer l'âge au moment de l'évaluation
player_data = creer_colonne_age_au_moment(player_data, "birthday", "date")

# Garder les colonnes utiles
attributs_physiques = ["acceleration", "strength", "stamina"]
player_data = select_colonnes(player_data, ["age"] + attributs_physiques)

# Créer les tranches d'âge
player_data = creer_tranche_age(player_data, "age")

# Calculer les moyennes
age_group_avg = player_data.groupby("age_group")[attributs_physiques].mean()

# Afficher les résultats
print(age_group_avg)

# Visualisation
age_group_avg.plot(kind="bar", figsize=(10, 6))
plt.title(
    "Moyenne des attributs physiques par groupe d'âge "
    "(au moment de l'évaluation)"
)
plt.ylabel("Valeur moyenne des attributs")
plt.xlabel("Tranche d'âge")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
