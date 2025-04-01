import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV
df_stats = pd.read_csv("data/Player_Attributes.csv")
df_noms = pd.read_csv("data/Player.csv")

# Liste des joueurs déjà sélectionnés pour éviter les doublons
joueurs_selectionnes = set()

# Définir les postes et leurs critères
postes_criteres = {
    "GK": [
        "gk_diving",
        "gk_handling",
        "gk_kicking",
        "gk_positioning",
        "gk_reflexes",
    ],
    "DD": [
        "stamina",
        "aggression",
        "interceptions",
        "standing_tackle",
        "sliding_tackle",
        "sprint_speed",
        "acceleration",
        "agility",
    ],
    "DG": [
        "stamina",
        "aggression",
        "interceptions",
        "standing_tackle",
        "sliding_tackle",
        "sprint_speed",
        "acceleration",
        "agility",
    ],
    "DCD": [
        "aggression",
        "interceptions",
        "standing_tackle",
        "sliding_tackle",
        "jumping",
        "strength",
        "marking",
    ],
    "DCG": [
        "aggression",
        "interceptions",
        "standing_tackle",
        "sliding_tackle",
        "jumping",
        "strength",
        "marking",
    ],
    "MDC1": [
        "short_passing",
        "long_passing",
        "ball_control",
        "aggression",
        "interceptions",
        "positioning",
        "vision",
        "standing_tackle",
        "sliding_tackle",
    ],
    "MDC2": [
        "short_passing",
        "long_passing",
        "ball_control",
        "aggression",
        "interceptions",
        "positioning",
        "vision",
        "standing_tackle",
        "sliding_tackle",
    ],
    "AD": [
        "crossing",
        "finishing",
        "short_passing",
        "dribbling",
        "curve",
        "free_kick_accuracy",
        "long_passing",
        "ball_control",
        "acceleration",
        "sprint_speed",
        "agility",
        "stamina",
        "long_shots",
    ],
    "AG": [
        "crossing",
        "finishing",
        "short_passing",
        "dribbling",
        "curve",
        "free_kick_accuracy",
        "long_passing",
        "ball_control",
        "acceleration",
        "sprint_speed",
        "agility",
        "stamina",
        "long_shots",
    ],
    "BU1": [
        "finishing",
        "heading_accuracy",
        "dribbling",
        "volleys",
        "curve",
        "acceleration",
        "sprint_speed",
        "reactions",
        "shot_power",
        "penalties",
    ],
    "BU2": [
        "finishing",
        "heading_accuracy",
        "dribbling",
        "volleys",
        "curve",
        "acceleration",
        "sprint_speed",
        "reactions",
        "shot_power",
        "penalties",
    ],
}

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

# Positionnement des joueurs sur un schéma de terrain en 4-4-2
positions = {
    "GK": (5, 1),
    "DD": (9, 3),
    "DG": (1, 3),
    "DCD": (3.6, 3),
    "DCG": (6.4, 3),
    "MDC1": (3, 5),
    "MDC2": (7, 5),
    "AD": (9, 7),
    "AG": (1, 7),
    "BU1": (4, 9),
    "BU2": (6, 9),
}

# Création du terrain
fig, ax = plt.subplots(figsize=(6, 9))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Colorier le fond en vert
fig.patch.set_facecolor("green")
ax.set_facecolor("green")

# Tracer les lignes du terrain en blanc
for line in [
    ([0, 10], [5, 5]),  # Ligne du milieu
    ([2.5, 7.5], [8, 8]),  # Surface adverse
    ([2.5, 7.5], [2, 2]),  # Surface gardien
    ([0, 0], [0, 10]),  # Bord gauche
    ([10, 10], [0, 10]),  # Bord droit
    ([0, 10], [10, 10]),  # Ligne de but haute
    ([0, 10], [0, 0]),  # Ligne de but basse
]:
    plt.plot(line[0], line[1], color="white", linewidth=2)

# Affichage des joueurs
for _, row in df_meilleur_11.iterrows():
    poste = row["Poste"]
    x, y = positions[poste]

    ax.scatter(
        x, y, s=600, color="blue", edgecolors="white", linewidth=2
    )  # Point du joueur
    ax.text(
        x,
        y + 0.4,
        row["nom"],
        fontsize=10,
        ha="center",
        color="black",
        fontweight="bold",
    )  # Nom au-dessus
    ax.text(
        x, y - 0.6, row["prenom"], fontsize=9, ha="center", color="black"
    )  # Prénom en dessous

# Masquer les axes
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)

plt.title("Formation 4-4-2", fontsize=14, color="black", fontweight="bold")
plt.show()
