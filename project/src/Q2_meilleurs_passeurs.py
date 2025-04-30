from project.src.fonctions_communes import (
    lire_csv,
    transforme,
    compter_actions_par_joueur,
    trier_joueurs_par_actions,
)

# Charger les données
match = lire_csv("data/Match.csv")
player = lire_csv("data/Player.csv")

# Filtrer le championnat et la saison souhaités
match = match[(match["goal"].notna()) & (match["goal"] != "")]
match = match[match["season"] == "2015/2016"]
# match = match[match["country_id"] == "1729"]  # facultatif si tu veux filtrer
# par championnat

# Transformer les colonnes goal en DataFrames
goals_transformed = [transforme(g) for g in match["goal"]]

# Compter les buts par joueur (player1)
buts_par_joueur = compter_actions_par_joueur(goals_transformed, "player2")

# Obtenir le top 10 des buteurs
top_passeur = trier_joueurs_par_actions(buts_par_joueur, player, top_n=10)

# Afficher le classement
print(top_passeur)
