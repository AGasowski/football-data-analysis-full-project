import pandas as pd


def championnat(nom_championnat):
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
    # Obtenir l'ID du championnat
    id_league = championnat(championnat_nom)
    if id_league is None:
        return []

    # Charger les données
    matches_df = pd.read_csv("data/Match.csv")
    teams_df = pd.read_csv("data/Team.csv")

    # Filtrer les matchs
    matches_filtrés = matches_df[
        (matches_df["league_id"] == id_league)
        & (matches_df["season"] == saison)
    ]

    # Obtenir les IDs uniques
    equipes_ids = pd.unique(
        matches_filtrés[
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
