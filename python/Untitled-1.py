
import pandas as pd

def transformer_player_attributes(df):
    # S'assurer que 'player_api_id' et 'overall_rating' existent
    if "player_api_id" not in df.columns or "overall_rating" not in df.columns:
        raise ValueError("La table doit contenir les colonnes 'player_api_id' et 'overall_rating'")

    # Convertir la colonne 'date' en datetime
    df["date"] = pd.to_datetime(df["date"])

    # Extraire la saison (par exemple "2014/2015")
    def get_saison(date):
        year = date.year
        return f"{year}/{year+1}" if date.month >= 7 else f"{year-1}/{year}"

    df["saison"] = df["date"].apply(get_saison)

    # Garder la ligne avec le meilleur overall_rating pour chaque joueur et chaque saison
    df_max = (
        df.sort_values(["player_api_id", "saison", "overall_rating"], ascending=[True, True, False])
          .drop_duplicates(subset=["player_api_id", "saison"], keep="first")
          .copy()
    )

    # Générer toutes les combinaisons possibles joueur × saison
    saisons = [f"{y}/{y+1}" for y in range(2007, 2016)]
    joueurs = df["player_api_id"].unique()
    full_index = pd.MultiIndex.from_product([joueurs, saisons], names=["player_api_id", "saison"])
    df_complet = pd.DataFrame(index=full_index).reset_index()

    # Fusionner pour compléter les saisons manquantes
    df_result = pd.merge(df_complet, df_max[["player_api_id", "saison", "overall_rating"]],
                         on=["player_api_id", "saison"], how="left")

    # Remplir les valeurs manquantes par la dernière valeur connue (forward fill)
    df_result = df_result.sort_values(["player_api_id", "saison"])
    df_result["overall_rating"] = df_result.groupby("player_api_id")["overall_rating"].ffill()

    return df_result
df = pd.read_csv("data/Player_Attributes.csv")
df_corrige = transformer_player_attributes(df)
print(df_corrige.head())