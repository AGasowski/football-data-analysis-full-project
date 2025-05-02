import pandas as pd
from collections import defaultdict

# Gérer des opérations générales sur DataFrame et dict, notamment le filtrage,
# les jointures et les conversions.


# Opérations sur les DataFrames
def filtrer_df(df, filtre_col=None, filtre_val=None, colonnes=None):
    """
    Filtre et sélectionne des colonnes dans un DataFrame.

    Paramètres:
    -----------
    df : pd.DataFrame
        Le DataFrame à traiter.
    filtre_col : str, optional
        Nom de la colonne sur laquelle filtrer.
    filtre_val : any, optional
        Valeur pour le filtrage.
    colonnes : list of str, optional
        Colonnes à sélectionner après filtrage.

    Retour:
    -------
    pd.DataFrame ou pd.Series
    """
    if filtre_col and filtre_val is not None:
        df = df[df[filtre_col] == filtre_val]
    if colonnes:
        return df[colonnes] if len(colonnes) > 1 else df[colonnes[0]]
    return df


def fusionner(df1, df2, col1, col2):
    return pd.merge(
        df1,
        df2,
        left_on=col1,
        right_on=col2,
        how="inner",
    )


def id_en_nom(match, team):
    """
    Remplace les IDs d'équipes par leurs noms dans un DataFrame de matchs.

    Paramètres
    ----------
    match : pandas.DataFrame
        DataFrame contenant les colonnes 'home_team_api_id' et
        'away_team_api_id'.
    team : pandas.DataFrame
        DataFrame avec les colonnes 'team_api_id' et 'team_long_name'.

    Retourne
    -------
    None
    """
    match["home_team_api_id"] = (
        match["home_team_api_id"]
        .map(team.set_index("team_api_id")["team_long_name"])
        .fillna(match["home_team_api_id"])
    )
    match["away_team_api_id"] = (
        match["away_team_api_id"]
        .map(team.set_index("team_api_id")["team_long_name"])
        .fillna(match["away_team_api_id"])
    )
    match.rename(columns={"home_team_api_id": "home_team"}, inplace=True)
    match.rename(columns={"away_team_api_id": "away_team"}, inplace=True)


# Gestion de dictionnaires
def creer_dict(nb_val):
    """
    Crée un dictionnaire avec des listes de zéros de longueur nb_val comme
    valeur par défaut.

    Paramètres
    ----------
    nb_val : int
        Nombre d'éléments par défaut dans la liste associée à chaque clé.

    Retourne
    -------
    defaultdict
        Dictionnaire avec des listes de zéros comme valeur par défaut.
    """
    dict = defaultdict(lambda: [0] * nb_val)
    return dict


def name_team_dic(team_names, team_id):
    """
    Retourne le nom d'une équipe à partir de son identifiant.

    Paramètres : - team_names (dict) : Dictionnaire associant les identifiants
    d'équipes à leurs noms. - team_id (int ou str) : Identifiant de l'équipe
    recherchée.

    Retour : - str : Nom de l'équipe correspondant à l'identifiant, ou
    "Inconnu" si l'identifiant n'est pas trouvé.
    """
    try:
        team_id = int(team_id)
    except ValueError:
        return "Inconnu"
    return team_names.get(team_id, "Inconnu")


def cles_dic(dic):
    """
    Retourne les clés d'un dictionnaire.

    Paramètres : - dic (dict) : Dictionnaire dont on veut obtenir les clés.

    Retour : - dict_keys : Objet contenant les clés du dictionnaire.
    """
    return dic.keys()


def filtre_dic(dic, ind_col, val_col):
    """
    Filtre un dictionnaire pour ne garder que les éléments dont une certaine
    valeur correspond à un critère donné.

    Paramètres : - dic (dict) : Dictionnaire à filtrer. Les valeurs sont
    supposées être des séquences ou des listes. - ind_col (int) : Index dans la
    valeur à tester. - val_col (any) : Valeur recherchée à la position ind_col.

    Retour : - dict : Dictionnaire filtré ne contenant que les éléments
    répondant au critère.
    """
    dic = {k: v for k, v in dic.items() if v[ind_col] == val_col}
    return dic


def ratio_dic(dic, id, ind_val1, ind_val2):
    """
    Calcule le ratio entre deux valeurs d'une entrée du dictionnaire,
    identifiée par une clé.

    Paramètres : - dic (dict) : Dictionnaire contenant les données. Les valeurs
    sont des séquences (ex. : listes). - id (hashable) : Clé de l'entrée pour
    laquelle on veut effectuer l'opération. - ind_val1 (int) : Index de la
    valeur à utiliser en numérateur. - ind_val2 (int) : Index de la valeur à
    utiliser en dénominateur.

    Retour : - float : Résultat de la division si possible, sinon 0 (en cas de
    division par zéro).
    """
    ratio = (
        dic[id][ind_val1] / dic[id][ind_val2] if dic[id][ind_val2] > 0 else 0
    )
    return ratio


def cle_extreme(dic, type_extremum="max"):
    """
    Retourne la clé de la valeur maximale ou minimale d'un dictionnaire.

    Paramètres:
    -----------
    dic : dict
        Dictionnaire à analyser.
    type_extremum : str ("max" ou "min")
        Type d'extrême recherché.

    Retour:
    -------
    Clé avec la valeur extrême.
    """
    if not dic:
        raise ValueError("Dictionnaire vide")
    if type_extremum == "max":
        return max(dic, key=dic.get)
    elif type_extremum == "min":
        return min(dic, key=dic.get)
    else:
        raise ValueError("Type non supporté")


def appliquer_fonction_aux_valeurs(d, f):
    """
    Applique une fonction à chaque valeur d’un dictionnaire et renvoie un
    nouveau dictionnaire.

    Paramètres
    ----------
    d : dict
        Dictionnaire dont les valeurs seront transformées.

    f : callable
        Fonction à appliquer à chaque valeur du dictionnaire.

    Retourne
    --------
    dict
        Nouveau dictionnaire avec les mêmes clés et les valeurs transformées
        par la fonction.
    """
    return {k: f(v) for k, v in d.items()}
