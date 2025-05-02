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
        if date.month >= 8:  # Août à Décembre => saison commence cette année
            return f"{year}-{year + 1}"
        else:  # Janvier à Juillet => saison commence l'année précédente
            return f"{year - 1}-{year}"

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


print(process_player_attributes("data/Player_Attributes.csv"))
