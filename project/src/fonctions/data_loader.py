import pandas as pd
import xml.etree.ElementTree as ET
import csv


# Charger des données (CSV/XML) et les convertir en formats utiles (DataFrame,
# dict, list, etc.).


# Chargement des données
def charger_csv(chemin, mode="dataframe", cle_id=None, *noms_champs):
    """
    Charge un fichier CSV et le retourne sous forme de DataFrame ou de
    dictionnaire.

    Paramètres:
    -----------
    chemin : str
        Chemin du fichier CSV à charger.
    mode : str, optional ("dataframe" ou "dict")
        Mode de chargement : DataFrame (par défaut) ou dictionnaire.
    cle_id : str, optional
        Nom de la colonne utilisée comme clé si mode='dict'.
    *noms_champs : str
        Champs à inclure dans le dictionnaire si mode='dict'.

    Retour:
    -------
    pd.DataFrame ou dict
    """
    if mode == "dataframe":
        df = pd.read_csv(chemin)
        return df
    elif mode == "dict" and cle_id:
        data_dict = {}
        with open(chemin, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                identifiant = int(row[cle_id])
                valeurs = tuple(row[nom] for nom in noms_champs)
                data_dict[identifiant] = (
                    valeurs[0] if len(valeurs) == 1 else valeurs
                )
        return data_dict
    else:
        raise ValueError("Mode invalide ou paramètres manquants.")


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
        }
        stats = value.find("stats")
        if stats is not None:
            entry.update({f"stats_{child.tag}": child.text for child in stats})
            data.append(entry)
    df = pd.DataFrame(data)
    return df


# Conversion de structures
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
    return dict(zip(df[col_a], df[col_b]))


def convertir_colonne(df, col, type_cible):
    """
    Convertit une colonne d'un DataFrame en un type donné.

    Paramètres:
    -----------
    df : pd.DataFrame
        DataFrame contenant la colonne.
    col : str
        Nom de la colonne à convertir.
    type_cible : str ("int" ou "list")
        Type cible de la conversion.

    Retour:
    -------
    list si type_cible == 'list', sinon None (conversion in-place).
    """
    if type_cible == "int":
        df[col] = df[col].astype(int)
    elif type_cible == "list":
        return df[col].tolist()
    else:
        raise ValueError("Type de conversion non supporté.")


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
