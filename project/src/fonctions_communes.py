import pandas as pd
import locale
import platform
import xml.etree.ElementTree as ET
import csv
from collections import defaultdict


# Fonctions pour importer un csv
def lire_csv(chemin):
    """
    Lit un fichier CSV à l'aide de pandas et retourne un DataFrame.
    """
    return pd.read_csv(chemin)


def lire_csv_en_dict(chemin, cle_id, *noms_champs):
    """
    Lit un fichier CSV et retourne un dictionnaire structuré à partir d'un
    identifiant unique et de champs spécifiés.

    Paramètres
    ----------
    chemin : str
        Le chemin d'accès au fichier CSV à lire.
    cle_id : str
        Le nom de la colonne à utiliser comme identifiant unique (clé du
        dictionnaire).
    *noms_champs : str
        Un ou plusieurs noms de colonnes dont les valeurs doivent être
        extraites pour chaque ligne.

    Retour
    ------
    dict
        Un dictionnaire dont les clés sont les identifiants (convertis en int)
        extraits de la colonne `cle_id`, et les valeurs : - un simple élément
        si un seul champ est spécifié ; - un tuple si plusieurs champs sont
        spécifiés.
    """
    data_dict = {}
    with open(chemin, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            identifiant = int(row[cle_id])
            valeurs = tuple(row[nom] for nom in noms_champs)
            if len(valeurs) == 1:
                valeurs = valeurs[0]  # Si un seul champ, pas besoin de tuple
            data_dict[identifiant] = valeurs
    return data_dict


# Fonctions pour bien régler le format de la date
def convertir_date(df):
    """
    Convertit la colonne 'date' d'un DataFrame en format datetime, puis
    applique une configuration de date en français.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant une colonne 'date' sous forme de chaînes de
        caractères.

    Retourne
    -------
    pandas.DataFrame
        Le DataFrame avec la colonne 'date' convertie en datetime.
    """
    df["date"] = pd.to_datetime(df["date"])
    date_francais()
    return df


def date_format(date):
    """
    Formate une date en français avec le jour, le mois et l’année.

    Paramètres
    ----------
    date : datetime.datetime
        Date à formater.

    Retourne
    -------
    str
        Date formatée sous forme : 'lundi 01 janvier 2024'.
    """
    return date.strftime("%A %d %B %Y")


def date_francais():
    """
    Configure la locale en français, compatible Windows, Linux et macOS. Ne pas
    ajouter au code car elle est déjà incluse dans la fonction convertir_date()
    """
    systeme = platform.system()

    try:
        if systeme == "Windows":
            locale.setlocale(locale.LC_TIME, "French_France.1252")
        else:  # Linux ou macOS
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        print(
            "Impossible de définir la locale française. Elle n’est "
            "peut-être pas installée sur ce système."
        )


# Fonctions pour sélectionner des lignes/colonnes
def select_colonnes(df, liste):
    """
    Sélectionne un sous-ensemble de colonnes dans un DataFrame pandas.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame à partir duquel on souhaite extraire des colonnes.

    liste : list of str
        Une liste des noms de colonnes à sélectionner.

    Retour
    ------
    pd.DataFrame
        Un nouveau DataFrame contenant uniquement les colonnes spécifiées.
    """
    return df[liste]


def select(df, col1, val_col1, *cols):
    """
    Filtre un DataFrame sur une condition d'égalité et sélectionne une ou
    plusieurs colonnes.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame à filtrer.

    col1 : str
        Le nom de la colonne sur laquelle appliquer la condition d'égalité.

    val_col1 : any
        La valeur à rechercher dans la colonne `col1`.

    *cols : str
        Un ou plusieurs noms de colonnes à retourner après filtrage.

    Retour
    ------
    pd.Series ou pd.DataFrame
        Une série si une seule colonne est sélectionnée, sinon un DataFrame
        contenant les colonnes spécifiées après filtrage.
    """
    return df[df[col1] == val_col1][list(cols)]


def select_all(df, col, val_col):
    """
    Filtre un DataFrame en ne gardant que les lignes où une colonne donnée est
    égale à une valeur spécifiée.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame à filtrer.

    col : str
        Le nom de la colonne sur laquelle appliquer la condition.

    val_col : any
        La valeur à rechercher dans la colonne `col`.

    Retour
    ------
    pd.DataFrame
        Un DataFrame ne contenant que les lignes pour lesquelles la colonne
        `col` est égale à `val_col`.
    """
    return df[df[col] == val_col]


# Convertir le type des colonnes d'un DataFrame
def convertir_int(df, col):
    """
    Convertit une colonne d'un DataFrame en entier.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant la colonne à convertir.
    col : str
        Nom de la colonne à convertir en int.

    Retourne
    -------
    None
    """
    df[col] = df[col].astype(int)


def convertir_list(df, col):
    """
    Convertit une colonne d'un DataFrame en liste Python.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant la colonne.
    col : str
        Nom de la colonne à convertir.

    Retourne
    -------
    list
        Liste des valeurs de la colonne.
    """
    return df[col].tolist()


# Calculs à partir des valeurs d'un Dataframe
def diff_abs(df, a, b):
    """
    Calcule la différence absolue entre deux colonnes.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant les colonnes.
    a : str
        Nom de la première colonne.
    b : str
        Nom de la seconde colonne.

    Retourne
    -------
    pandas.Series
        Série contenant la différence absolue entre les deux colonnes.
    """
    return abs(df[a] - df[b])


def max_col(df, col):
    """
    Retourne la valeur maximale d'une colonne.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant la colonne.
    col : str
        Nom de la colonne.

    Retourne
    -------
    valeur
        Valeur maximale dans la colonne spécifiée.
    """
    return df[col].max()


# Fonctions de fusion
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


def fusionner(df1, df2, col1, col2):
    return pd.merge(
        df1,
        df2,
        left_on=col1,
        right_on=col2,
        how="inner",
    )


# Fonctions d'affichage
def afficher(resultat):
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
    print(resultat.to_string(index=False))


# Fonctions liées au groupe_by
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


# Fonctions pour la manipulation de dictionnaires
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


# Fonctions pour la manipulation de listes
def trier_liste_tuples(L, ind):
    """
    Trie une liste de tuples (ou listes) en place selon l'élément à une
    position donnée.

    Paramètres : - L (list) : Liste de tuples ou de listes à trier. - ind (int)
    : Index de l'élément dans les tuples à utiliser pour le tri.

    Effet de bord : - La liste L est triée en place par ordre décroissant selon
    l'élément à l'indice ind.

    Retour : - Aucun (le tri est fait en place).
    """
    L.sort(key=lambda x: x[ind], reverse=True)


# Fonctions plus spécifiques
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


def transforme(X):
    """
    Convertit un code XML en DataFrame pandas.

    Paramètres:
    -----------
    X : str
        Une chaîne de caractères contenant un document XML.

    Retourne:
    ---------
    pd.DataFrame
        Un DataFrame contenant les données extraites du XML, avec les attributs
        des éléments "value" comme colonnes et les sous-éléments de "stats"
        préfixés par "stats_".

    Exemples:
    ---------
    ```python xml_data = \"\"\"<root>
        <value>
            <name>John</name> <age>30</age> <stats>
                <height>180</height> <weight>75</weight>
            </stats>
        </value> <value>
            <name>Jane</name> <age>28</age> <stats>
                <height>165</height> <weight>60</weight>
            </stats>
        </value>
    </root>\"\"\"

    df = transforme(xml_data) print(df) ``` Résultat : ```
       name age  stats_height  stats_weight
    0  John  30          180            75 1  Jane  28          165 60 ```
    """
    root = ET.fromstring(X)
    data = []
    for value in root.findall("value"):
        entry = {
            child.tag: child.text for child in value if child.tag != "stats"
        }  # Exclure stats pour l'instant
        stats = value.find("stats")  # Extraire les stats
        if stats is not None:
            entry.update({f"stats_{child.tag}": child.text for child in stats})
            data.append(entry)
    # Convertir en DataFrame
    df = pd.DataFrame(data)
    return df


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


# Fonctions El Hadji


def fusionner_colonnes_en_listes(df, colonnes):
    """
    Fusionne les valeurs de plusieurs colonnes sélectionnées d’un DataFrame
    ligne par ligne.

    Paramètres:
    -----------
    df : pandas.DataFrame
        Le DataFrame contenant les données d’entrée.

    colonnes : list of str
        Liste des noms de colonnes du DataFrame à fusionner. Les colonnes
        doivent exister dans le DataFrame. Chaque ligne des colonnes
        sélectionnées sera transformée en une liste.

    Retourne:
    ---------
    list of list
        Une liste de listes, où chaque sous-liste contient les valeurs d’une
        ligne pour les colonnes spécifiées.
    """
    if not all(col in df.columns for col in colonnes):
        raise ValueError(
            "Une ou plusieurs colonnes spécifiées n'existent pas dans le "
            "DataFrame."
        )

    return df[colonnes].apply(lambda row: list(row), axis=1).tolist()


def cle_maximale(D):
    """
    Renvoie la clé associée à la plus grande valeur dans un dictionnaire.

    Paramètres
    ----------
    D : dict
        Dictionnaire dont les valeurs sont comparables (int, float, etc.).

    Retourne
    --------
    key
        La clé correspondant à la valeur maximale dans le dictionnaire.

    Lève
    -----
    ValueError
        Si le dictionnaire est vide.
    """
    if not D:
        raise ValueError("Le dictionnaire est vide.")

    return max(D, key=D.get)


def cle_minimale(D):
    """
    Renvoie la clé associée à la plus petite valeur dans un dictionnaire.

    Paramètres
    ----------
    D : dict
        Dictionnaire dont les valeurs sont comparables (int, float, etc.).

    Retourne
    --------
    key
        La clé correspondant à la valeur maximale dans le dictionnaire.

    Lève
    -----
    ValueError
        Si le dictionnaire est vide.
    """
    if not D:
        raise ValueError("Le dictionnaire est vide.")

    return min(D, key=D.get)


def moyenne_liste(L):
    """
    Calcule la moyenne des éléments d'une liste de nombres.

    Paramètres
    ----------
    L : list of int or float
        Liste contenant des valeurs numériques.

    Retourne
    --------
    float
        La moyenne arithmétique des éléments de la liste.

    Lève
    -----
    ValueError
        Si la liste est vide.
    """
    if not L:
        raise ValueError("La liste est vide.")

    return sum(L) / len(L)


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


def element_min_colonne(df, col_b, col_a):
    """
    Renvoie l'élément de la colonne 'col_a' où la valeur correspondante dans la
    colonne 'col_b' est minimale.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant les colonnes spécifiées.

    col_b : str
        Le nom de la colonne dans le DataFrame où la valeur minimale sera
        recherchée.

    col_a : str
        Le nom de la colonne dans le DataFrame dont l'élément sera renvoyé pour
        la ligne où la valeur de 'col_b' est minimale.

    Retourne
    -------
    element : type de l'élément dans 'col_a'
        L'élément de la colonne 'col_a' correspondant à la ligne où la colonne
        'col_b' a la valeur minimale. Si plusieurs éléments ont la même valeur
        minimale dans 'col_b', l'élément de la première ligne est retourné.

    Exemple
    -------
    >>> df = pd.DataFrame({'A': [10, 20, 30, 40], 'B': [5, 2, 9, 1]})
    >>> element_min_colonne(df, 'B', 'A')
    40

    L'exemple ci-dessus retourne '40' car la valeur minimale de la colonne 'B'
    est '1', et l'élément correspondant de la colonne 'A' à cet index est '40'.
    """
    # Trouver l'index de la valeur minimale dans la colonne spécifiée 'col_b'
    idx_min = df[col_b].idxmin()
    # Retourner l'élément correspondant dans la colonne spécifiée 'col_a'
    return df.loc[idx_min, col_a]


def data_to_dict(df, col_a, col_b):
    """
    Crée un dictionnaire à partir de deux colonnes d'un DataFrame où chaque
    élément de la première colonne devient une clé et l'élément correspondant
    de la seconde colonne devient la valeur associée.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant les colonnes spécifiées.

    col_a : str
        Le nom de la colonne dont les éléments seront utilisés comme clés dans
        le dictionnaire.

    col_b : str
        Le nom de la colonne dont les éléments seront utilisés comme valeurs
        dans le dictionnaire.

    Retourne
    -------
    dict
        Un dictionnaire où les clés sont les éléments de la colonne `col_a` et
        les valeurs sont les éléments correspondants de la colonne `col_b`.

    Exemple
    -------
    >>> df = pd.DataFrame({'A': ['a', 'b', 'c', 'd'], 'B': [1, 2, 3, 4]})
    >>> creer_dictionnaire(df, 'A', 'B')
    {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    L'exemple ci-dessus retourne un dictionnaire où les éléments de la colonne
    'A' sont utilisés comme clés et ceux de la colonne 'B' comme valeurs.
    """
    # Crée le dictionnaire à partir des colonnes A et B
    return dict(zip(df[col_a], df[col_b]))


def moyenne_par_colonne(df, col_1, col_2):
    """
    Crée un dictionnaire où chaque clé est un identifiant (col_1) et la valeur
    est la moyenne des valeurs de la colonne (col_2) associées à cet
    identifiant.

    Paramètres
    ----------
    df : pandas.DataFrame
        DataFrame contenant les colonnes spécifiées.

    col_1 : str
        Nom de la colonne représentant les identifiants (par exemple, 'id').

    col_2 : str
        Nom de la colonne représentant les valeurs à agréger (par exemple,
        'ratio').

    Retourne
    -------
    dict
        Un dictionnaire où chaque clé est un identifiant et chaque valeur est
        la moyenne des valeurs associées à cet identifiant dans la colonne
        `col_2`.
    """
    # Calcul de la moyenne des valeurs dans col_2 pour chaque identifiant dans
    # col_1
    moyenne_values = df.groupby(col_1)[col_2].mean().to_dict()

    return moyenne_values


# Fonctions Chahid


def trier_dict(data, cles, reverse=True):
    """
    Trie un dictionnaire selon une ou plusieurs clés internes.

    Paramètres
    ----------
    dict : dict
        Dictionnaire dont les valeurs sont elles-mêmes des dictionnaires
        contenant les clés de tri. Par exemple : {"PSG": {"points": 80,
        "goal_diff": 45}, ...}
    clés : list of str
        Liste des clés internes servant à trier les éléments du dictionnaire.
        Le tri se fait dans l’ordre des clés fournies (de la plus prioritaire à
        la moins prioritaire).
    reverse : bool, optional
        Si True (par défaut), effectue un tri décroissant. Si False, le tri est
        croissant.

    Retourne
    -------
    dict
        Nouveau dictionnaire trié selon les critères donnés, avec les paires
        clé/valeur dans l’ordre défini.
    """
    return dict(
        sorted(
            data.items(),
            key=lambda item: tuple(item[1][key] for key in cles),
            reverse=reverse,
        )
    )


def moyenne(L):
    return sum(L) / len(L)


def get_taille_joueurs(player_df, player_api_id):
    """
    Récupère le poids d'un joueur en fonction de son ID.

    Paramètres : player_df (DataFrame) : Le DataFrame contenant les
    informations sur les joueurs. player_api_id (int) : L'ID du joueur pour
    lequel on veut obtenir le poids.

    Retour : float ou None : Le poids du joueur si trouvé, sinon None.
    """
    # Recherche du joueur dans le DataFrame en fonction de son player_api_id
    player_row = player_df[player_df["player_api_id"] == player_api_id]

    if not player_row.empty:
        return player_row["weight"].values[0]  # Retourne le poids du joueur
    else:
        return None  # Si le joueur n'est pas trouvé, on retourne None


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
                player_ids = convertir_list(goal_df, "player1")
                subtypes = convertir_list(goal_df, "subtype")

                # Recherche des joueurs ayant marqué du type voulu
                for pid, sub in zip(player_ids, subtypes):
                    if sub == subtype and pid not in scorers:
                        scorers.append(int(pid))

    return scorers


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
            player_ids = convertir_list(df, colonne)
            for pid in player_ids:
                try:
                    pid = int(pid)
                    compteur[pid] = compteur.get(pid, 0) + 1
                except ValueError:
                    continue  # ignore les valeurs non convertibles

    return compteur


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


def filtre_cartons(card, type_carton):
    carton = []
    for df in card:
        if isinstance(df, pd.DataFrame):
            if "card_type" in df.columns:
                try:
                    filtered = select_all(df, "card_type", type_carton)
                    carton.append(filtered)
                except KeyError:
                    pass  # Sécurité en cas d'erreur imprévue
    return carton
