import pandas as pd

# import numpy as np
# from sklearn.model_selection import train_test_split

df_equipe = pd.read_pickle('enfin.pkl')
df_match = pd.read_pickle('match.pkl')

print(df_match)
"""
# Jointure pour les équipes à domicile
df_match = df_match.merge(
    df_equipe,
    left_on=["home_team_api_id", "season"],
    right_on=["team_api_id", "saison"],
    how="left",
    suffixes=("", "_h"),  # Ajoute le suffixe _h pour éviter les conflits
)

# Renommage des colonnes pour l'équipe à domicile
df_match = df_match.rename(
    columns=lambda x: (
        x + "_h" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x
    )
)

# Jointure pour les équipes à l'extérieur
df_match = df_match.merge(
    df_equipe,
    left_on=["away_team_api_id", "season"],
    right_on=["team_api_id", "saison"],
    how="left",
    suffixes=("", "_a"),
)

# Renommage des colonnes pour l'équipe à l'extérieur
df_match = df_match.rename(
    columns=lambda x: (
        x + "_a" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x
    )
)


print(df_match.columns, df_match.head())

X = df_final.drop(columns=["final_position"])
y = df_final["final_position"]



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""
