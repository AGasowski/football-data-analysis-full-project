import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches  # Importation de patches
from project.src.fonctions.manipulations import filtrer_df
from operator import itemgetter


# Fonctions plus spécifiques


# Affichage et tri
def afficher(resultat, head=True):
    """
    Affiche un DataFrame sans les index, sous forme de texte.

    Paramètres
    ----------
    resultat : pandas.DataFrame
        Le DataFrame à afficher.

    Retourne
    -------
    None
    """
    print(resultat.to_string(index=False, header=head))


def trier(data, par=None, type_data="liste", reverse=True):
    """
    Trie une liste, un dictionnaire ou un DataFrame.

    Paramètres:
    -----------
    data : list, dict ou pd.DataFrame
        Données à trier.
    par : int, str ou list
        Clé ou index de tri.
    type_data : str ("liste", "dict", "dataframe")
        Type de données à trier.
    reverse : bool, optional
        Tri décroissant (True par défaut).

    Retour:
    -------
    Tri en place ou nouveau dictionnaire/DataFrame trié.
    """
    if type_data == "liste":
        data.sort(key=lambda x: x[par], reverse=reverse)
    elif type_data == "dict":
        # Si par est un entier (on trie par la valeur du dictionnaire)
        if isinstance(par, int):
            return dict(
                sorted(data.items(), key=lambda item: item[1], reverse=reverse)
            )
        # Si par est un itérable, on trie par les clés multiples
        return dict(
            sorted(
                data.items(),
                key=lambda item: tuple(item[1][k] for k in par),
                reverse=reverse,
            )
        )
    elif type_data == "dataframe":
        return data.sort_values(by=par, ascending=not reverse)
    else:
        raise ValueError("Type de donnée non supporté pour le tri")


# Spécifique au football
def formation(L):
    """
    Détermine la formation tactique d'une équipe à partir des abscisses des
    joueurs.

    Paramètres:
    -----------
    L : list of int or float
        Liste triée des abscisses (coordonnées X) des 11 joueurs d’une équipe
        sur le terrain. Chaque valeur représente la position horizontale d’un
        joueur. Les joueurs sont triés dans l’ordre croissant de leur abscisse
        pour un traitement correct.

    Retourne:
    ---------
    list of int
        Une liste contenant le nombre de joueurs présents à chaque position
        horizontale unique. Cela correspond à une décomposition de la formation
        tactique.

    Exemples:
    ---------
    ```python abscisses = [2, 2, 2, 2, 4, 4, 6, 6, 6, 8, 10]
    formation(abscisses) ```

    Résultat : ```python [4, 2, 3, 1, 1] ``` Ce qui signifie : 4 joueurs sur la
    première ligne (souvent la défense), 2 sur la suivante, 3 au milieu, etc.
    """
    formation1 = []
    C = L[0]
    j = 0
    for i in range(len(L)):
        if L[i] != C:
            formation1.append(j)
            j = 1
            C = L[i]
        else:
            j += 1
    formation1.append(j)
    return formation1


def get_taille_joueurs(player_df, player_api_id):
    """
    Récupère la taille d'un joueur en fonction de son ID.

    Paramètres : player_df (DataFrame) : Le DataFrame contenant les
    informations sur les joueurs. player_api_id (int) : L'ID du joueur pour
    lequel on veut obtenir la taille.

    Retour : float ou None : La taille du joueur si trouvé, sinon None.
    """
    player_row = player_df[player_df["player_api_id"] == player_api_id]

    if not player_row.empty:
        return player_row["height"].values[0]
    else:
        return None


def filtre_cartons(card, type_carton):
    carton = []
    for df in card:
        if isinstance(df, pd.DataFrame):
            if "card_type" in df.columns:
                try:
                    filtered = filtrer_df(df, "card_type", type_carton)
                    carton.append(filtered)
                except KeyError:
                    pass  # Sécurité en cas d'erreur imprévue
    return carton


# Spécifique Q7


def choix_criteres():
    """
    Retourne un dictionnaire associant chaque poste de football à une liste de
    critères (caractéristiques) nécessaires pour évaluer les joueurs à ce
    poste.

    Retourne
    -------
    dict
        Dictionnaire des postes et de leurs critères associés.
    """
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


def nom_prenom(df):
    """
    Sépare le champ "player_name" d'un DataFrame en deux colonnes "prenom" et
    "nom". Si le nom ne contient qu'un seul mot, il est mis dans 'nom' et
    'prenom' est vide.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant une colonne 'player_name'.

    Retourne
    -------
    pd.DataFrame
        DataFrame avec les colonnes 'prenom' et 'nom' ajoutées.
    """

    def separer_nom_prenom(nom_complet):
        parties = nom_complet.strip().split()
        if len(parties) == 1:
            return pd.Series(["", parties[0]])  # prenom vide, nom = mot unique
        else:
            return pd.Series([" ".join(parties[:-1]), parties[-1]])

    df[["prenom", "nom"]] = df["player_name"].apply(separer_nom_prenom)
    return df


def list_en_df(L, *cols):
    """
    Convertit un dictionnaire en DataFrame avec noms de colonnes personnalisés.

    Paramètres
    ----------
    L : dict
        Dictionnaire à transformer.
    *cols : str
        Deux noms de colonnes pour le DataFrame.

    Retourne
    -------
    pd.DataFrame
        DataFrame avec deux colonnes correspondant aux clés et valeurs du
        dictionnaire.
    """
    if len(cols) != 2:
        raise ValueError("Tu dois fournir exactement deux noms de colonnes.")
    df = pd.DataFrame(list(L.items()), columns=list(cols))
    return df


def filtrer_par_pied(df, poste):
    """
    Filtre les joueurs selon le pied préféré en fonction de leur poste.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame des joueurs.
    poste : str
        Poste à évaluer.

    Retourne
    -------
    pd.DataFrame
        DataFrame filtré selon le pied préféré.
    """
    poste_droit = ["DD", "DCD", "AD"]
    poste_gauche = ["DG", "DCG", "AG"]

    if poste in poste_droit:
        return df[df["preferred_foot"].str.lower() == "right"]
    elif poste in poste_gauche:
        return df[df["preferred_foot"].str.lower() == "left"]
    else:
        return df


def calcul_scores_postes(df, dic):
    """
    Calcule un score total par poste pour chaque joueur à partir des critères
    définis.

    Paramètres
    ----------
    df : pd.DataFrame
        DataFrame contenant les statistiques des joueurs.
    dic : dict
        Dictionnaire des postes et des critères associés.

    Retourne
    -------
    pd.DataFrame
        DataFrame avec colonnes supplémentaires pour les scores par poste.
    """
    for poste, criteres in dic.items():
        df[poste + "_score"] = df[criteres].sum(axis=1)
    return df


def trouver_joueur_poste(df_stats, poste, joueurs_selectionnes):
    """
    Trouve l'ID du meilleur joueur pour un poste donné sans doublons.

    Paramètres
    ----------
    df_stats : pd.DataFrame
        DataFrame avec les scores des joueurs.
    poste : str
        Poste à pourvoir.
    joueurs_selectionnes : set
        Ensemble des IDs déjà sélectionnés.

    Retourne
    -------
    int or None
        ID du joueur sélectionné ou None si aucun disponible.
    """
    df_filtre = filtrer_par_pied(df_stats, poste)
    df_filtre = df_filtre.sort_values(by=poste + "_score", ascending=False)

    for _, row in df_filtre.iterrows():
        joueur_id = row["player_api_id"]
        if joueur_id not in joueurs_selectionnes:
            return joueur_id
    return None  # Aucun joueur disponible


def terrain(df_meilleur_11, chemin_sortie):
    """
    Affiche une représentation graphique d'un terrain de football avec les
    joueurs placés en formation 4-4-2.

    Paramètres
    ----------
    df_meilleur_11 : pd.DataFrame
        DataFrame contenant les colonnes 'Poste', 'nom', 'prenom' pour chaque
        joueur sélectionné.

    Retourne
    -------
    None
    """
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

    # Enregistrement
    plt.savefig(chemin_sortie, bbox_inches="tight", dpi=300)
    print(f"Terrain enregistré dans {chemin_sortie}")

    plt.show()


# Spécifique Q10


def visualisation(age_group_avg):
    age_group_avg.plot(kind="bar", figsize=(10, 6))
    plt.title(
        "Moyenne des attributs physiques par groupe d'âge "
        "(au moment de l'évaluation)"
    )
    plt.ylabel("Valeur moyenne des attributs")
    plt.xlabel("Tranche d'âge")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("output/q10/aptitudes_age.png", bbox_inches="tight", dpi=300)
    print("Graphique enregistré dans 'output/q10/aptitudes_age.png' ")
    plt.show()


# Spécifiques Q8


def afficher_top_clubs_regularite(df, top_n=10):
    """Affiche les top N clubs avec les joueurs les plus réguliers."""
    # Renommer les colonnes
    df = df.rename(
        columns={
            "team_long_name": "Equipe",
            "tech_std": "Moyenne des écarts-types des performances",
        }
    )

    # Réinitialiser l'index pour affichage propre avec classement
    df = df.reset_index(drop=True)
    df.index += 1  # Le classement commence à 1

    # Affichage
    print(
        f"Top {top_n} clubs les plus réguliers (selon les 11 joueurs les "
        f"plus utilisés) :\n"
    )
    print(
        df[["Equipe", "Moyenne des écarts-types des performances"]].head(top_n)
    )


def tri_bet(df):
    df_new = sorted(df, key=itemgetter("Cote_VainqueurB365"), reverse=True)
    return df_new
