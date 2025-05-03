"""
Script pour déterminer les clubs qui ont un 11 plus régulier en terme de
performances que les autres.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.statistiques import (
    nettoyer_attributs_techniques,
    calculer_ecart_type_technique_par_joueur,
    moyenne_ecart_type_par_joueur,
    construire_compteur_joueurs,
    extraire_top_joueurs_par_club,
    calculer_consistance_club,
)
from project.src.fonctions.utils import afficher_top_clubs_regularite


def run_q8():
    """
    Affiche le classement des équipes avec le 11 le plus régulier en terme de
    performances. On choisit pour chaque équipe les 11 joueurs les plus
    souvent alignés sur le terrain.
    """

    print("==================================================================")
    print("         Classement des équipes les plus régulières")
    print("==================================================================")
    # Chargement
    player_attr = charger_csv("data/Player_Attributes.csv")
    matchs = charger_csv("data/Match.csv")
    teams = charger_csv("data/Team.csv")

    # Attributs techniques utilisés
    tech_attrs = [
        "ball_control",
        "short_passing",
        "long_passing",
        "dribbling",
        "vision",
        "finishing",
        "crossing",
    ]

    # Traitement
    player_attr = nettoyer_attributs_techniques(player_attr, tech_attrs)
    player_attr = calculer_ecart_type_technique_par_joueur(
        player_attr, tech_attrs
    )
    player_std_by_player = moyenne_ecart_type_par_joueur(player_attr)

    compteur = construire_compteur_joueurs(matchs)
    club_player_df = extraire_top_joueurs_par_club(compteur)
    club_consistency = calculer_consistance_club(
        club_player_df, player_std_by_player, teams
    )

    # Affichage
    afficher_top_clubs_regularite(club_consistency)
