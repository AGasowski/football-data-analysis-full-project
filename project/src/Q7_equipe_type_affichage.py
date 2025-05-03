"""
Script pour sélectionner et afficher le meilleur 11 de football en formation
4-4-2.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.dates_formats import convertir_date
from project.src.fonctions.manipulations import (
    fusionner,
    filtrer_df,
    get_saison,
)
from project.src.fonctions.utils import (
    terrain,
    choix_criteres,
    nom_prenom,
    list_en_df,
    trouver_joueur_poste,
    calcul_scores_postes,
)


def run_q7(saison):
    """
    Affiche le meilleur onze (11) de football pour une saison donnée en
    formation 4-4-2.

    Ce script sélectionne les meilleurs joueurs pour chaque poste, puis les
    affiche dans une formation 4-4-2.

    Args:
        saison (str): Saison ciblée, ex. "2007/2008". Si "0", tous les matchs
        sont pris en compte.
    """
    print("==================================================================")
    print(f"          Equipe type de la saison {saison}")
    print("==================================================================")

    # Charger le fichier CSV
    df_stats = charger_csv("data/Player_Attributes.csv")
    df_noms = charger_csv("data/Player.csv")

    df_stats = convertir_date(df_stats)

    if saison != "0":
        df_stats = get_saison(df_stats)
        df_stats = filtrer_df(df_stats, "saison", saison)

    # Liste des joueurs déjà sélectionnés pour éviter les doublons
    joueurs_selectionnes = set()

    # Définir les postes et leurs critères
    postes_criteres = choix_criteres()

    # Calculer tous les scores en une seule fois pour éviter les erreurs de
    # colonne manquante
    df_stats = calcul_scores_postes(df_stats, postes_criteres)

    # Sélection des meilleurs joueurs par poste
    meilleur_11 = {}

    for poste in postes_criteres:
        joueur = trouver_joueur_poste(df_stats, poste, joueurs_selectionnes)
        if joueur is not None:
            meilleur_11[poste] = joueur
            joueurs_selectionnes.add(joueur)

    # Convertir en DataFrame pour fusionner avec les noms
    df_meilleur_11 = list_en_df(meilleur_11, "Poste", "player_api_id")

    # Joindre avec le fichier des noms
    df_meilleur_11 = fusionner(
        df_meilleur_11, df_noms, "player_api_id", "player_api_id"
    )

    # Affichage de l'équipe
    print("Meilleur 11 en 4-4-2 entre 2007 et 2016:")
    for _, row in df_meilleur_11.iterrows():
        print(f"{row['Poste']}: {row['player_name']}")

    # Séparer le nom complet en prénom et nom
    df_meilleur_11 = nom_prenom(df_meilleur_11)

    # Afficher l'équipe sur le terrain
    terrain(df_meilleur_11)
