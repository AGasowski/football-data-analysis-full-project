import pandas as pd
from datetime import datetime


def process_player_attributes(chemin_csv):
    # Lecture du fichier
    df = pd.read_csv(chemin_csv)

    # Conversion de la colonne date
    df["date"] = pd.to_datetime(df["date"])

    # Création de la colonne saison
    def get_season(date):
        year = date.year
        if date.month >= 6:  # Août à Décembre => saison commence cette année
            return f"{year}/{year + 1}"
        else:  # Janvier à Juillet => saison commence l'année précédente
            return f"{year - 1}/{year}"

    df["saison"] = df["date"].apply(get_season)

    # Prendre la overall_rating maximale par joueur et par saison
    df_max = (
        df.groupby(["player_api_id", "saison"])["overall_rating"].max().reset_index()
    )

    # Liste de toutes les saisons dans l'ensemble de données
    toutes_saisons = sorted(df_max["saison"].unique())

    # Liste complète de joueurs
    tous_joueurs = df_max["player_api_id"].unique()

    # Création d’un DataFrame avec toutes les combinaisons joueur-saison
    full_index = pd.MultiIndex.from_product(
        [tous_joueurs, toutes_saisons], names=["player_api_id", "saison"]
    )
    full_df = pd.DataFrame(index=full_index).reset_index()

    # Merge avec les données réelles
    full_df = full_df.merge(df_max, on=["player_api_id", "saison"], how="left")

    # Remplissage des valeurs manquantes avec la overall_rating de la saison précédente
    full_df = full_df.sort_values(by=["player_api_id", "saison"])
    full_df["overall_rating"] = full_df.groupby("player_api_id")[
        "overall_rating"
    ].ffill()

    return full_df

def moyenne(liste):
    propre = [x for x in liste if x is not None]
    if propre:
        return sum(propre) / len(propre)
    else:
        return None 

import pandas as pd
from datetime import datetime

def process_player_attributes1(chemin_csv, player_csv):
    # Lecture des fichiers
    df = pd.read_csv(chemin_csv)
    player_df = pd.read_csv(player_csv)

    # Convertir les dates
    df["date"] = pd.to_datetime(df["date"])
    player_df["birthday"] = pd.to_datetime(player_df["birthday"])

    # Fonction pour obtenir la saison
    def get_season(date):
        year = date.year
        if date.month >= 6:
            return f"{year}/{year + 1}"
        else:
            return f"{year - 1}/{year}"

    df["saison"] = df["date"].apply(get_season)

    # Max du rating par joueur et saison
    df_max = (
        df.groupby(["player_api_id", "saison"])["overall_rating"].max().reset_index()
    )

    # Toutes saisons et joueurs
    toutes_saisons = sorted(df_max["saison"].unique())
    tous_joueurs = df_max["player_api_id"].unique()

    # Produit croisé
    full_index = pd.MultiIndex.from_product(
        [tous_joueurs, toutes_saisons], names=["player_api_id", "saison"]
    )
    full_df = pd.DataFrame(index=full_index).reset_index()

    # Merge et remplissage
    full_df = full_df.merge(df_max, on=["player_api_id", "saison"], how="left")
    full_df = full_df.sort_values(by=["player_api_id", "saison"])
    full_df["overall_rating"] = full_df.groupby("player_api_id")["overall_rating"].ffill()

    # Ajout date de naissance
    full_df = full_df.merge(player_df[["player_api_id", "birthday"]], on="player_api_id", how="left")

    # Calcul de l'âge au 1er août de l'année de début de saison
    def saison_to_start_date(saison):
        start_year = int(saison.split("/")[0])
        return datetime(start_year, 8, 1)

    full_df["season_start"] = full_df["saison"].apply(saison_to_start_date)
    full_df["age"] = (
        (full_df["season_start"] - full_df["birthday"]).dt.days // 365
    )

    # Optionnel : supprimer colonne temporaire
    full_df.drop(columns=["season_start"], inplace=True)

    return full_df

