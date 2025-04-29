import pandas as pd
from fonctions_communes import lire_csv
from Q7_fonctions import terrain, choix_criteres

# Charger le fichier CSV
df_stats = lire_csv("data/Player_Attributes.csv")
df_noms = lire_csv("data/Player.csv")

# Liste des joueurs déjà sélectionnés pour éviter les doublons
joueurs_selectionnes = set()

# Définir les postes et leurs critères
postes_criteres = choix_criteres()

# Calculer tous les scores en une seule fois pour éviter les erreurs de colonne
# manquante
for poste, criteres in postes_criteres.items():
    df_stats[poste + "_score"] = df_stats[criteres].sum(axis=1)

# Sélection des meilleurs joueurs par poste
meilleur_11 = {}

for poste, criteres in postes_criteres.items():
    # Appliquer un filtre selon le poste
    if poste in ["DD", "DCD", "AD"]:
        df_selection = df_stats[
            df_stats["preferred_foot"].str.lower() == "right"
        ]
    elif poste in ["DG", "DCG", "AG"]:
        df_selection = df_stats[
            df_stats["preferred_foot"].str.lower() == "left"
        ]
    else:
        df_selection = df_stats

    # Trier par score et exclure les joueurs déjà sélectionnés
    df_selection = df_selection.sort_values(
        by=poste + "_score", ascending=False
    )

    # Trouver le premier joueur disponible
    for _, row in df_selection.iterrows():
        joueur_id = row["player_api_id"]
        if joueur_id not in joueurs_selectionnes:
            meilleur_11[poste] = joueur_id
            joueurs_selectionnes.add(
                joueur_id
            )  # Ajouter aux joueurs sélectionnés
            break  # Sortir dès qu'on a trouvé un joueur valide

# Convertir en DataFrame pour fusionner avec les noms
df_meilleur_11 = pd.DataFrame(
    list(meilleur_11.items()), columns=["Poste", "player_api_id"]
)

# Joindre avec le fichier des noms
df_meilleur_11 = df_meilleur_11.merge(
    df_noms[["player_api_id", "player_name"]], on="player_api_id", how="left"
)

# Affichage de l'équipe
print("Meilleur 11 en 4-4-2 entre 2007 et 2016:")
for _, row in df_meilleur_11.iterrows():
    print(f"{row['Poste']}: {row['player_name']}")


# Séparer le nom complet en prénom et nom
df_meilleur_11[["prenom", "nom"]] = df_meilleur_11["player_name"].str.rsplit(
    " ", n=1, expand=True
)

terrain(df_meilleur_11)
