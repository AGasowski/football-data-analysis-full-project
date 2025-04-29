import pandas as pd

# Charger les données (remplace 'fichier.csv' par le chemin de ton fichier)
df = pd.read_csv("data/Match.csv")

print(df["date"].head())
