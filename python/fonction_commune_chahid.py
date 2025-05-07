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


def id_en_nom_2(classement, team):
    classement["team_api_id"] = (
        classement[int("team_api_id")]
        .map(team.set_index("team_api_id")["team_long_name"])
        .fillna(classement["team_api_id"])
    )
    classement.rename(columns={"team_api_id": "team"}, inplace=True)


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


def creer_dict_2(cles):
    """
    Crée un dictionnaire avec des clés dynamiques et un dictionnaire de zéros
    comme valeur par défaut pour chaque entrée.

    Paramètres
    ----------
    nb_val : int
        (Non utilisé ici, gardé si besoin dans le futur)
    cles : list
        Liste des clés à utiliser dans chaque valeur par défaut.

    Retourne
    -------
    defaultdict
        Dictionnaire avec, pour chaque nouvelle clé, un sous-dictionnaire contenant
        les clés de `cles` initialisées à zéro.
    """
    return defaultdict(lambda: {cle: 0 for cle in cles})


def name_team_dic(team_names, team_id):
    """
    Retourne le nom d'une équipe à partir de son identifiant.

    Paramètres : - team_names (dict) : Dictionnaire associant les identifiants
    d'équipes à leurs noms. - team_id (int ou str) : Identifiant de l'équipe
    recherchée.

    Retour : - str : Nom de l'équipe correspondant à l'identifiant, ou
    "Inconnu" si l'identifiant n'est pas trouvé.
    """
    team_name = team_names.get(team_id, "Inconnu")
    return team_name


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

    Paramètres : - L (list) : Liste de tuples ou de listes à trier.
    - ind (int) : Index de l'élément dans les tuples à utiliser pour le tri.

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


def trier_dict(data, cles, reverse=True):
    """
    Trie un dictionnaire selon une ou plusieurs clés internes.

    Paramètres
    ----------
    dict : dict
        Dictionnaire dont les valeurs sont elles-mêmes des dictionnaires contenant
        les clés de tri. Par exemple : {"PSG": {"points": 80, "goal_diff": 45}, ...}
    clés : list of str
        Liste des clés internes servant à trier les éléments du dictionnaire.
        Le tri se fait dans l’ordre des clés fournies (de la plus prioritaire à la moins prioritaire).
    reverse : bool, optional
        Si True (par défaut), effectue un tri décroissant. Si False, le tri est croissant.

    Retourne
    -------
    dict
        Nouveau dictionnaire trié selon les critères donnés, avec les paires clé/valeur
        dans l’ordre défini.
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

    Paramètres :
    player_df (DataFrame) : Le DataFrame contenant les informations sur les joueurs.
    player_api_id (int) : L'ID du joueur pour lequel on veut obtenir le poids.

    Retour :
    float ou None : Le poids du joueur si trouvé, sinon None.
    """
    # Recherche du joueur dans le DataFrame en fonction de son player_api_id
    player_row = player_df[player_df["player_api_id"] == player_api_id]

    if not player_row.empty:
        return player_row["weight"].values[0]  # Retourne le poids du joueur
    else:
        return None  # Si le joueur n'est pas trouvé, on retourne None


def get_scorers_by_subtype(goals_df_list, subtype):
    """
    Renvoie la liste des joueurs ayant marqué un but d'un certain type (ex : 'header').

    Paramètres :
    - goals_df_list (list) : Liste de DataFrames représentant les buts (résultats de transforme()).
    - subtype (str) : Le type de but recherché (ex : 'header').

    Retour :
    - list : Liste des IDs des joueurs ayant marqué avec le subtype donné.
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

    Paramètres :
    - goal_dfs (list) : Liste de DataFrames (résultat de transforme()).
    - colonne (str) : Le nom de la colonne où figure l'identifiant du joueur (ex : 'player1' ou 'assist').

    Retour :
    - dict : Dictionnaire {player_id: count}
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
    Trie les joueurs selon leur nombre d'actions (but, passe, etc.) et ajoute leur nom.

    Paramètres :
    - compteur (dict) : Dictionnaire {player_id: count}
    - player_df (DataFrame) : Table des joueurs (doit contenir player_api_id et player_name)
    - top_n (int) : Nombre de joueurs à afficher (default = 10)

    Retour :
    - DataFrame : Classement des joueurs
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


import pandas as pd

team = pd.read_csv("data/Team.csv")
id_team = [g for g in team["team_api_id"]]
nom_team = [g for g in team["team_long_name"]]


def id_to_nom(id):
    team = pd.read_csv("data/Team.csv")
    id_team = [g for g in team["team_api_id"]]
    nom_team = [g for g in team["team_long_name"]]
    for i in range(len(id_team)):
        if id_team[i] == id:
            return nom_team[i]


def calculer_classement(df_match, saison, league_id):
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
