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
    Lit un fichier CSV sans pandas et retourne un dictionnaire : - La clé est
    la valeur de la colonne `cle_id`. - La valeur est soit :
        - un seul champ (si un seul nom est donné)
        - un tuple de champs (si plusieurs noms sont donnés)
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
    df["date"] = pd.to_datetime(df["date"])
    date_francais()
    return df


def date_francais():
    """
    Configure la locale en français, compatible Windows, Linux et macOS.
    Ne pas ajouter au code car elle est déjà incluse dans la fonction
    convertir_date()
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


def select(df, col1, val_col1, col2):
    """
    Filtre un DataFrame sur une condition et sélectionne une colonne
    spécifique.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame à filtrer.

    col1 : str
        Le nom de la colonne sur laquelle appliquer la condition d'égalité.

    val_col1 : any
        La valeur à rechercher dans la colonne `col1`.

    col2 : str
        Le nom de la colonne à retourner après filtrage.

    Retour
    ------
    pd.Series
        Une série contenant les valeurs de la colonne `col2` pour lesquelles la
        colonne `col1` est égale à `val_col1`.
    """
    return df[df[col1] == val_col1][col2]


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


def creer_dict(nb_val):
    dict = defaultdict(lambda: [0] * nb_val)
    return dict


def convertir_int(df, col):
    df[col] = df[col].astype(int)


def convertir_list(df, col):
    return df[col].tolist()


def diff_abs(df, a, b):
    return abs(df[a] - df[b])


def max_col(df, col):
    return df[col].max()


def id_en_nom(match, team):
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


def afficher(resultat):
    print(resultat.to_string(index=False))


def nb_occurences(df, col):
    return df.groupby(col).size()


def max_serie(df):
    return df.idxmax(), df.max()


def date_format(date):
    return date.strftime("%A %d %B %Y")


def compter_buts_matchs(dic, goals, ind_team, ind_goal):
    for val in dic.values():
        team = int(val[ind_team])
        goal = int(val[ind_goal])

        if team in goals:
            goals[team][0] += goal
        else:
            goals[team][0] = goal
        goals[team][1] += 1
    return goals


def fusionner(df1, df2, col1, col2):
    return pd.merge(
        df1,
        df2,
        left_on=col1,
        right_on=col2,
        how="inner",
    )


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
