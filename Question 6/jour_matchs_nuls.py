from fonctions_utiles_panda import (
    lire_csv,
    convertir_date,
    date_francais,
    select_all,
    select,
)

# Charger les données (remplace 'fichier.csv' par le chemin de ton fichier)
match = lire_csv("data/Match.csv")

# Modifier la colonne 'date' en format datetime et en français
convertir_date(match)
date_francais()

# Filtrer les matchs nuls
matchs_nuls = select_all(match, "home_team_goal", match["away_team_goal"])

# Compter le nombre de matchs nuls par jour
matchs_nuls_par_jour = matchs_nuls.groupby("date").size()

print(matchs_nuls_par_jour)

# Trouver le jour avec le plus de matchs nuls
jour_max_matchs_nuls = matchs_nuls_par_jour.idxmax()
nombre_max_nuls = matchs_nuls_par_jour.max()

# Supposons que jour_max_matchs_nuls = datetime(2009, 2, 14)
date_formatee = jour_max_matchs_nuls.strftime("%A %d %B %Y")

# Mettre la première lettre en majuscule
date_formatee = date_formatee.capitalize()

print(date_formatee)

print(
    f"Le jour avec le plus de matchs nuls est : {date_formatee} avec "
    f"{nombre_max_nuls} matchs nuls."
)
