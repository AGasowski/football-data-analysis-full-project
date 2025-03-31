import pandas as pd
import locale

# Charger les données (remplace 'fichier.csv' par le chemin de ton fichier)
df = pd.read_csv("data/Match.csv")

# Assurer que la colonne 'date' est bien en format datetime
df["date"] = pd.to_datetime(df["date"])

# Filtrer les matchs nuls
matchs_nuls = df[df["home_team_goal"] == df["away_team_goal"]]

# Compter le nombre de matchs nuls par jour
matchs_nuls_par_jour = matchs_nuls.groupby("date").size()

# Trouver le jour avec le plus de matchs nuls
jour_max_matchs_nuls = matchs_nuls_par_jour.idxmax()
nombre_max_nuls = matchs_nuls_par_jour.max()

# Définir la langue en français
locale.setlocale(locale.LC_TIME, "French_France.1252")

# Supposons que jour_max_matchs_nuls = datetime(2009, 2, 14)
date_formatee = jour_max_matchs_nuls.strftime("%A %d %B %Y")

# Mettre la première lettre en majuscule
date_formatee = date_formatee.capitalize()

print(date_formatee)

print(
    f"Le jour avec le plus de matchs nuls est : {date_formatee} avec "
    f"{nombre_max_nuls} matchs nuls."
)
