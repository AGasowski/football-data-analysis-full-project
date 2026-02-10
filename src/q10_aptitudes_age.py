"""
Script pour analyser les attributs physiques moyens des joueurs par tranche
d'âge.
"""

from src.fonctions.utils import (
    visualisation,
)
from src.fonctions.dates_formats import (
    convertir_col_date,
    convertir_date,
)
from src.fonctions.data_loader import charger_csv
from src.fonctions.manipulations import (
    fusionner,
    filtrer_df,
    creer_tranche_age,
    creer_colonne_age_au_moment,
)


def run_q10():
    """
    Calcule et affiche la moyenne des attributs physiques par tranche d'âge.
    """
    print("==================================================================")
    print("    Evolution des aptitudes des joueurs par catégories d'âge")
    print("==================================================================")

    # Charger les données
    player_attributes = charger_csv("data/Player_Attributes.csv")
    players = charger_csv("data/Player.csv")

    # Fusionner les tables pour avoir la date de naissance
    player_data = fusionner(
        player_attributes, players, "player_api_id", "player_api_id"
    )

    # Convertir les dates
    player_data = convertir_date(player_data)  # convertit la colonne 'date'
    player_data = convertir_col_date(
        player_data, "birthday"
    )  # convertit 'birthday'

    # Calculer l'âge au moment de l'évaluation
    player_data = creer_colonne_age_au_moment(player_data, "birthday", "date")

    # Garder les colonnes utiles
    attributs_physiques = ["acceleration", "strength", "stamina"]
    player_data = filtrer_df(
        player_data, None, None, ["age"] + attributs_physiques
    )

    # Créer les tranches d'âge
    player_data = creer_tranche_age(player_data, "age")

    # Calculer les moyennes
    age_group_avg = player_data.groupby("age_group")[
        attributs_physiques
    ].mean()

    # Afficher les résultats
    print(age_group_avg)

    # Visualisation
    visualisation(age_group_avg)
