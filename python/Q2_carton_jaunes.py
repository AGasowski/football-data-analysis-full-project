from fonction_commune_chahid import *

# Charger les données
match = lire_csv("data/Match.csv")
player = lire_csv("data/Player.csv")

# Filtrer le championnat et la saison souhaités
match = match[(match["goal"].notna()) & (match["goal"] != "")]
match = match[match["season"] == "2015/2016"]
# match = match[match["country_id"] == "1729"]  # facultatif si tu veux filtrer par championnat

# Transformer les colonnes goal en DataFrames
card = [transforme(g) for g in match["card"]]

carton_jaune_dfs = []
for df in card:
    if isinstance(df, pd.DataFrame):
        if "card_type" in df.columns:
            try:
                filtered = select_all(df, "card_type", "y")
                carton_jaune_dfs.append(filtered)
            except KeyError:
                pass  # Sécurité en cas d'erreur imprévue

# Étape 2 : utiliser la fonction générique
jaunes_par_joueur = compter_actions_par_joueur(carton_jaune_dfs, "player1")
top_jaunes = trier_joueurs_par_actions(jaunes_par_joueur, player, top_n=10)
print(top_jaunes)
