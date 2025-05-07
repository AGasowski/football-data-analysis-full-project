"""
Module : statistiques_football

Ce module contient diverses fonctions pour analyser et traiter des données
footballistiques issues de fichiers CSV. Les principales fonctionnalités
incluent des calculs de statistiques simples (moyennes, résumés), des analyses
de performance d'équipes et de joueurs, ainsi que des classements de
championnats.
"""

import pandas as pd
from project.src.fonctions.manipulations import creer_dict, fusionner
from project.src.fonctions.data_loader import convertir_colonne

# Faire des statistiques simples à partir de données : moyennes, résumés,
# classements...


# Statistiques générales
def calculer_moyenne(source, group_by_col=None, value_col=None):
    """
    Calcule une moyenne sur une liste ou un DataFrame groupé.

    Paramètres:
    -----------
    source : list ou pd.DataFrame
        Données d'entrée.
    group_by_col : str, optional
        Colonne d'identifiants pour le groupby (si DataFrame).
    value_col : str, optional
        Colonne des valeurs numériques (si DataFrame).

    Retour:
    -------
    float ou dict
    """
    if isinstance(source, list):
        if not source:
            raise ValueError("Liste vide")
        return sum(source) / len(source)
    if isinstance(source, pd.DataFrame) and group_by_col and value_col:
        return source.groupby(group_by_col)[value_col].mean().to_dict()
    raise ValueError("Paramètres incorrects pour le calcul de moyenne")


def resume_colonne(df, col_a, col_b=None, operation="max"):
    """
    Effectue un résumé statistique sur une colonne ou deux colonnes.

    Paramètres:
    -----------
    df : pd.DataFrame
        Données d'entrée.
    col_a : str
        Colonne principale.
    col_b : str, optional
        Deuxième colonne (utilisée pour certaines opérations).
    operation : str ("max", "min", "diff_abs")
        Type d'opération à effectuer.

    Retour:
    -------
    Résultat selon l’opération.
    """
    if operation == "max":
        return df[col_a].max()
    elif operation == "min":
        return df[col_a].min()
    elif operation == "diff_abs":
        return abs(df[col_a] - df[col_b])
    else:
        raise ValueError("Opération non supportée")


def nb_occurences(df, col):
    """
    Calcule le nombre d'occurrences de chaque valeur dans une colonne.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant la colonne.
    col : str
        Nom de la colonne.

    Retourne
    -------
    pandas.Series
        Série avec les valeurs uniques en index et le nombre d'occurrences en
        valeur.
    """
    return df.groupby(col).size()


def max_serie(df):
    """
    Retourne l'index et la valeur maximale de chaque colonne d'un DataFrame.

    Paramètres
    ----------
    df : pandas.DataFrame

    Retourne
    -------
    tuple
        Tuple contenant (index de la valeur max, valeur max) pour chaque
        colonne.
    """
    return df.idxmax(), df.max()


# Statistiques dédiées au football
def compter_buts_matchs(dic, goals, ind_team, ind_goal):
    """
    Compte les buts marqués et le nombre de matchs pour chaque équipe à partir
    d’un dictionnaire.

    Paramètres
    ----------
    dic : dict
        Dictionnaire contenant les données de match.
    goals : dict
        Dictionnaire où les résultats seront stockés (par équipe).
    ind_team : int
        Index de l’équipe dans la liste de valeurs.
    ind_goal : int
        Index du nombre de buts dans la liste de valeurs.

    Retourne
    -------
    dict
        Dictionnaire avec pour chaque équipe : [total_buts, nombre_de_matchs].
    """
    for val in dic.values():
        team = int(val[ind_team])
        goal = int(val[ind_goal])

        if team in goals:
            goals[team][0] += goal
            goals[team][1] += 1
        else:
            goals[team] = [goal, 1]
    return goals


def saison_equipe(matchs):
    """
    Calcule les statistiques des équipes à partir d'un dictionnaire de matchs.

    Paramètre : - matchs (dict) : Dictionnaire des matchs filtrés, où chaque
    valeur contient :
                      [season, league_id, home_team_api_id, away_team_api_id,
                      home_team_goal, away_team_goal]

    Retour : - stats (dict) : Dictionnaire associant chaque équipe à une liste
    de 3 éléments :
                     [points, buts marqués (BM), buts encaissés (BE)]
    """
    stats = creer_dict(3)
    for _, match in matchs.items():
        home_team_id = match[2]
        away_team_id = match[3]
        home_goals = int(match[4])
        away_goals = int(match[5])

        # Initialisation si les équipes ne sont pas encore dans stats
        for team_id in [home_team_id, away_team_id]:
            if team_id not in stats:
                stats[team_id] = [
                    0,
                    0,
                    0,
                ]  # [points, buts marqués, buts encaissés]

        # Mise à jour buts marqués et encaissés
        stats[home_team_id][1] += home_goals
        stats[home_team_id][2] += away_goals
        stats[away_team_id][1] += away_goals
        stats[away_team_id][2] += home_goals

        # Attribution des points
        if home_goals > away_goals:
            stats[home_team_id][0] += 3
        elif home_goals < away_goals:
            stats[away_team_id][0] += 3
        else:
            stats[home_team_id][0] += 1
            stats[away_team_id][0] += 1

    return stats


def calculer_classement(df_match, saison, league_id):
    """
    Calcule le classement des équipes pour une saison et une ligue données à
    partir des résultats des matchs.

    Paramètres:
    -----------
    df_match : pd.DataFrame
        DataFrame contenant les informations des matchs, y compris les colonnes
        suivantes : - 'season' : Saison du match - 'league_id' : Identifiant de
        la ligue - 'home_team_api_id' : Identifiant de l'équipe à domicile -
        'away_team_api_id' : Identifiant de l'équipe à l'extérieur -
        'home_team_goal' : Nombre de buts marqués par l'équipe à domicile -
        'away_team_goal' : Nombre de buts marqués par l'équipe à l'extérieur

    saison : str ou int
        La saison pour laquelle le classement doit être calculé (par exemple,
        "2020/2021").

    league_id : int
        L'identifiant de la ligue pour laquelle le classement doit être
        calculé.

    Retour:
    -------
    pd.DataFrame
        DataFrame contenant le classement des équipes avec les colonnes
        suivantes : - 'team_api_id' : Identifiant de l'équipe - 'points_total'
        : Nombre total de points obtenus - 'buts_marques' : Nombre total de
        buts marqués - 'buts_encaisses' : Nombre total de buts encaissés -
        'rank' : Rang de l'équipe dans le classement (ordre décroissant des
        points)

    Exemple:
    --------
    df_classement = calculer_classement(df_match, "2020/2021", 1)
    """
    # Filtrer les matchs de la saison et de la ligue
    df_filtre = df_match[
        (df_match["season"] == saison) & (df_match["league_id"] == league_id)
    ].copy()

    # Initialiser la liste des résultats
    classement = []

    for _, row in df_filtre.iterrows():
        home_id = row["home_team_api_id"]
        away_id = row["away_team_api_id"]
        home_goals = row["home_team_goal"]
        away_goals = row["away_team_goal"]

        # Attribution des points
        if home_goals > away_goals:
            points_home, points_away = 3, 0
        elif home_goals < away_goals:
            points_home, points_away = 0, 3
        else:
            points_home = points_away = 1

        # Ajouter les deux équipes dans le classement
        classement.append(
            {
                "team_api_id": home_id,
                "points": points_home,
                "buts_marques": home_goals,
                "buts_encaisses": away_goals,
            }
        )
        classement.append(
            {
                "team_api_id": away_id,
                "points": points_away,
                "buts_marques": away_goals,
                "buts_encaisses": home_goals,
            }
        )

    # Convertir en DataFrame
    df_resultats = pd.DataFrame(classement)

    # Agréger les résultats par équipe
    df_resultats = (
        df_resultats.groupby("team_api_id")
        .agg(
            points_total=("points", "sum"),
            buts_marques=("buts_marques", "sum"),
            buts_encaisses=("buts_encaisses", "sum"),
        )
        .reset_index()
    )

    # Calcul du classement (rang)
    df_resultats = df_resultats.sort_values(by="points_total", ascending=False)
    df_resultats["rank"] = (
        df_resultats["points_total"]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    return df_resultats


def compter_actions_par_joueur(goal_dfs, colonne):
    """
    Compte le nombre d'occurrences d'une action (but, passe, etc.) par joueur.

    Paramètres : - goal_dfs (list) : Liste de DataFrames (résultat de
    transforme()). - colonne (str) : Le nom de la colonne où figure
    l'identifiant du joueur (ex : 'player1' ou 'assist').

    Retour : - dict : Dictionnaire {player_id: count}
    """
    compteur = {}

    for df in goal_dfs:
        if isinstance(df, pd.DataFrame) and colonne in df.columns:
            player_ids = convertir_colonne(df, colonne, "list")
            for pid in player_ids:
                try:
                    pid = int(pid)
                    compteur[pid] = compteur.get(pid, 0) + 1
                except ValueError:
                    continue  # ignore les valeurs non convertibles

    return compteur


def get_scorers_by_subtype(goals_df_list, subtype):
    """
    Renvoie la liste des joueurs ayant marqué un but d'un certain type (ex :
    'header').

    Paramètres : - goals_df_list (list) : Liste de DataFrames représentant les
    buts (résultats de transforme()). - subtype (str) : Le type de but
    recherché (ex : 'header').

    Retour : - list : Liste des IDs des joueurs ayant marqué avec le subtype
    donné.
    """
    scorers = []

    for goal_df in goals_df_list:
        # Vérifie que c'est bien un DataFrame
        if isinstance(goal_df, pd.DataFrame):
            if "player1" in goal_df.columns and "subtype" in goal_df.columns:
                # Extraction des colonnes
                player_ids = convertir_colonne(goal_df, "player1", "list")
                subtypes = convertir_colonne(goal_df, "subtype", "list")

                # Recherche des joueurs ayant marqué du type voulu
                for pid, sub in zip(player_ids, subtypes):
                    if sub == subtype and pid not in scorers:
                        scorers.append(int(pid))

    return scorers


def trier_joueurs_par_actions(compteur, player_df, nom_action, top_n=10):
    """
    Trie les joueurs selon leur nombre d'actions (but, passe, etc.) et ajoute
    leur nom.

    Paramètres : - compteur (dict) : Dictionnaire {player_id: count} -
    player_df (DataFrame) : Table des joueurs (doit contenir player_api_id et
    player_name) - top_n (int) : Nombre de joueurs à afficher (default = 10)

    Retour : - DataFrame : Classement des joueurs avec nom et nombre d'actions
    """
    # Convertir le dictionnaire en DataFrame
    data = [
        {"player_api_id": pid, "nb_actions": nb}
        for pid, nb in compteur.items()
    ]
    df = pd.DataFrame(data)

    # Fusion avec les noms des joueurs
    fusion = fusionner(
        df,
        player_df[["player_api_id", "player_name"]],
        "player_api_id",
        "player_api_id",
    )

    # Trier par nombre d’actions décroissant
    fusion = fusion.sort_values(by="nb_actions", ascending=False).reset_index(
        drop=True
    )

    # Garder uniquement les colonnes utiles et renommer
    fusion = fusion[["player_name", "nb_actions"]].copy()
    fusion.columns = ["Joueur", nom_action]

    # Réinitialiser l'index pour faire un classement de 1 à top_n
    fusion.index += 1

    return fusion.head(top_n)


def nettoyer_attributs_techniques(df, colonnes):
    """Supprime les lignes avec des valeurs manquantes sur les attributs
    techniques."""
    return df.dropna(subset=colonnes)


def calculer_ecart_type_technique_par_joueur(df, colonnes):
    """Ajoute une colonne 'tech_std' : écart-type des attributs techniques par
    ligne."""
    df["tech_std"] = df[colonnes].std(axis=1)
    return df


def moyenne_ecart_type_par_joueur(df):
    """Calcule la moyenne des écarts-types pour chaque joueur."""
    return df.groupby("player_api_id")["tech_std"].mean().reset_index()


def construire_compteur_joueurs(matches):
    """Construit un dictionnaire : club → nombre d’apparitions de chaque
    joueur."""
    club_player_counts = {}
    for _, row in matches.iterrows():
        home_team = row["home_team_api_id"]
        away_team = row["away_team_api_id"]

        # Initialisation
        if home_team not in club_player_counts:
            club_player_counts[home_team] = {}
        if away_team not in club_player_counts:
            club_player_counts[away_team] = {}

        for i in range(1, 12):
            hp = row[f"home_player_{i}"]
            ap = row[f"away_player_{i}"]

            if pd.notna(hp):
                if hp not in club_player_counts[home_team]:
                    club_player_counts[home_team][hp] = 0
                club_player_counts[home_team][hp] += 1

            if pd.notna(ap):
                if ap not in club_player_counts[away_team]:
                    club_player_counts[away_team][ap] = 0
                club_player_counts[away_team][ap] += 1

    return club_player_counts


def extraire_top_joueurs_par_club(compteur, top_n=11):
    """Extrait les top N joueurs les plus utilisés pour chaque club."""
    club_player_pairs = []
    for club_id, joueurs in compteur.items():
        joueurs_tries = sorted(
            joueurs.items(), key=lambda x: x[1], reverse=True
        )[:top_n]
        for player_id, _ in joueurs_tries:
            club_player_pairs.append((club_id, player_id))
    return pd.DataFrame(
        club_player_pairs, columns=["team_api_id", "player_api_id"]
    )


def calculer_consistance_club(df_players, player_std_by_player, teams):
    """Calcule la moyenne des écarts-types pour chaque club, et ajoute le nom
    du club."""
    merged = df_players.merge(player_std_by_player, on="player_api_id")
    club_consistency = (
        merged.groupby("team_api_id")["tech_std"].mean().reset_index()
    )
    club_consistency = club_consistency.merge(
        teams[["team_api_id", "team_long_name"]], on="team_api_id"
    )
    return club_consistency.sort_values("tech_std")


def ecart_de_buts(match):
    """Calcule l'écart de buts entre l'équipe à domicile et l'équipe à
    l'extérieur dans un match.
    """
    try:
        return abs(int(match["home_team_goal"]) - int(match["away_team_goal"]))
    except (KeyError, ValueError, TypeError):
        return -1
