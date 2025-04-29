import matplotlib.pyplot as plt
import matplotlib.patches as patches  # Importation de patches


def choix_criteres():
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
    return postes_criteres


def terrain(df_meilleur_11):
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
        ([7.5, 7.5], [8, 10]),  # Surface adverse côté droit
        ([2.5, 2.5], [8, 10]),  # Surface adverse côté gauche
        ([2.5, 7.5], [2, 2]),  # Surface gardien
        ([7.5, 7.5], [0, 2]),  # Surface gardien côté droit
        ([2.5, 2.5], [0, 2]),  # Surface gardien côté gauche
        ([0, 0], [0, 10]),  # Bord gauche
        ([10, 10], [0, 10]),  # Bord droit
        ([0, 10], [10, 10]),  # Ligne de but haute
        ([0, 10], [0, 0]),  # Ligne de but basse
    ]:
        plt.plot(line[0], line[1], color="white", linewidth=2)

    # Ajouter un cercle blanc au milieu
    centre_cercle = plt.Circle(
        (5, 5), 1.3, color="white", fill=False, linewidth=2
    )
    ax.add_patch(centre_cercle)

    # Ajouter un arc de cercle aux surfaces
    arc_centre1 = patches.Arc(
        (5, 8),
        1.2,
        1.2,
        angle=180,
        theta1=0,
        theta2=180,
        color="white",
        linewidth=2,
    )
    ax.add_patch(arc_centre1)
    arc_centre2 = patches.Arc(
        (5, 2),
        1.2,
        1.2,
        angle=0,
        theta1=0,
        theta2=180,
        color="white",
        linewidth=2,
    )
    ax.add_patch(arc_centre2)

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

    # Affichage des joueurs
    for _, row in df_meilleur_11.iterrows():
        poste = row["Poste"]
        x, y = positions[poste]

        ax.scatter(
            x,
            y,
            s=600,
            color="blue",
            edgecolors="white",
            linewidth=2,
            zorder=4,
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
