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
    ratio = dic[id][ind_val1] / dic[id][ind_val2] if dic[id][ind_val2] > 0 else 0
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
    Détermine la formation tactique d'une équipe à partir des abscisses des joueurs.

    Paramètres:
    -----------
    L : list of int or float
        Liste triée des abscisses (coordonnées X) des 11 joueurs d’une équipe sur le terrain.
        Chaque valeur représente la position horizontale d’un joueur. Les joueurs sont                      
        triés dans l’ordre croissant de leur abscisse pour un traitement correct.

    Retourne:
    ---------
    list of int
        Une liste contenant le nombre de joueurs présents à chaque position horizontale unique.
        Cela correspond à une décomposition de la formation tactique.

    Exemples:
    ---------
    ```python
    abscisses = [2, 2, 2, 2, 4, 4, 6, 6, 6, 8, 10]
    formation(abscisses)
    ```

    Résultat :
    ```python
    [4, 2, 3, 1, 1]
    ```
    Ce qui signifie : 4 joueurs sur la première ligne (souvent la défense),
    2 sur la suivante, 3 au milieu, etc.
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
