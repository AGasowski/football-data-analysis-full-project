"""
Module : fonctions.names

Ce module fournit des fonctions utilitaires pour récupérer l'ID d'un
championnat à partir de son nom et pour obtenir la liste des équipes
participantes pour une saison donnée dans un championnat spécifique.
"""

import pandas as pd


def championnat(nom_championnat):
    """
    Renvoie l'ID d'un championnat en fonction de son nom.

    Args:
        nom_championnat (str): Le nom du championnat (par exemple, "Ligue 1
        (France)").

    Returns:
        int: L'ID du championnat si trouvé, sinon None.
    """
    championnats = {
        "Ligue 1 (France)": 4769,
        "Premier League (Angleterre)": 1729,
        "Bundesliga (Allemagne)": 7809,
        "Serie A (Italie)": 10257,
        "Liga BBVA (Espagne)": 21518,
        "Eredivisie (Pays-Bas)": 13274,
        "Liga ZON Sagres (Portugal)": 17642,
        "Ekstraklasa (Pologne)": 15722,
        "Jupiler League (Belgique)": 1,
        "Super League (Suisse)": 24558,
    }
    return championnats.get(nom_championnat, None)


def get_equipes_participantes(championnat_nom, saison):
    """
    Renvoie la liste des équipes participant à un championnat pour une saison
    donnée.

    Args:
        championnat_nom (str): Le nom du championnat (par exemple, "Ligue 1
        (France)"). saison (str): La saison sous la forme "AAAA/AAAA" (par
        exemple, "2014/2015").

    Returns:
        list: Une liste triée des noms des équipes participantes.
    """
    # Obtenir l'ID du championnat
    id_league = championnat(championnat_nom)
    if id_league is None:
        return []

    # Charger les données
    matches_df = pd.read_csv("data/Match.csv")
    teams_df = pd.read_csv("data/Team.csv")

    # Filtrer les matchs
    matches_filtres = matches_df[
        (matches_df["league_id"] == id_league)
        & (matches_df["season"] == saison)
    ]

    # Obtenir les IDs uniques
    equipes_ids = pd.unique(
        matches_filtres[
            ["home_team_api_id", "away_team_api_id"]
        ].values.ravel()
    )

    # Obtenir les noms des équipes à partir de leur ID
    equipes_participantes = (
        teams_df[teams_df["team_api_id"].isin(equipes_ids)]["team_long_name"]
        .dropna()
        .tolist()
    )

    return sorted(equipes_participantes)
