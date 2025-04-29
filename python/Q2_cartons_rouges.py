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

carton_rouge_dfs = []
for df in card:
    if isinstance(df, pd.DataFrame):
        if "card_type" in df.columns:
            try:
                filtered = select_all(df, "card_type", "r")
                carton_rouge_dfs.append(filtered)
            except KeyError:
                pass  # Sécurité en cas d'erreur imprévue

# Étape 2 : utiliser la fonction générique
rouges_par_joueur = compter_actions_par_joueur(carton_rouge_dfs, "player1")
top_rouges = trier_joueurs_par_actions(rouges_par_joueur, player, top_n=10)
print(top_rouges)
