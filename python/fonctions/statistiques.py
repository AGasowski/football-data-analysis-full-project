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
    elif isinstance(source, pd.DataFrame) and group_by_col and value_col:
        return source.groupby(group_by_col)[value_col].mean().to_dict()
    else:
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
        idx_min = df[col_b].idxmin()
        return df.loc[idx_min, col_a]
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
        else:
            goals[team][0] = goal
        goals[team][1] += 1
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
    for match_id, match in matchs.items():
        home_team_id = match[2]
        away_team_id = match[3]
        home_goals = int(match[4])
        away_goals = int(match[5])

        for team_id in [home_team_id, away_team_id]:
            if team_id not in stats:
                stats[team_id] = [
                    0,
                    0,
                    0,
                ]  # [points, goals_scored, goals_conceded]

        stats[home_team_id][1] += home_goals
        stats[home_team_id][2] += away_goals
        stats[away_team_id][1] += away_goals
        stats[away_team_id][2] += home_goals

        if home_goals > away_goals:
            stats[home_team_id][0] += 3
        elif home_goals < away_goals:
            stats[away_team_id][0] += 3
        else:
            stats[home_team_id][0] += 1
            stats[away_team_id][0] += 1
    return stats


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


def trier_joueurs_par_actions(compteur, player_df, top_n=10):
    """
    Trie les joueurs selon leur nombre d'actions (but, passe, etc.) et ajoute
    leur nom.

    Paramètres : - compteur (dict) : Dictionnaire {player_id: count} -
    player_df (DataFrame) : Table des joueurs (doit contenir player_api_id et
    player_name) - top_n (int) : Nombre de joueurs à afficher (default = 10)

    Retour : - DataFrame : Classement des joueurs
    """
    # Convertir le dictionnaire en DataFrame
    data = [
        {"player_api_id": pid, "nb_actions": nb}
        for pid, nb in compteur.items()
    ]
    df = pd.DataFrame(data)

    # Utiliser la fonction fusionner pour ajouter les noms des joueurs
    fusion = fusionner(
        df,
        player_df[["player_api_id", "player_name"]],
        "player_api_id",
        "player_api_id",
    )

    # Trier par nombre d’actions décroissant
    result = fusion.sort_values(by="nb_actions", ascending=False).reset_index(
        drop=True
    )

    return result.head(top_n)
