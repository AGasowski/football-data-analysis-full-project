import pandas as pd
import locale
import platform
import xml.etree.ElementTree as ET


def lire_csv(chemin):
    return pd.read_csv(chemin)


def convertir_date(df):
    df["date"] = pd.to_datetime(df["date"])
    return df


def date_francais():
    """Configure la locale en français, compatible Windows, Linux et macOS."""
    systeme = platform.system()

    try:
        if systeme == "Windows":
            locale.setlocale(locale.LC_TIME, "French_France.1252")
        else:  # Linux ou macOS
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        print(
            "⚠️ Impossible de définir la locale française. Elle n’est "
            "peut-être pas installée sur ce système."
        )


def select_variables(df, liste):
    return df[liste]


def fusionner(df1, df2, col1, col2):
    return pd.merge(
        df1,
        df2,
        left_on=col1,
        right_on=col2,
        how="inner",
    )


def select_saison(df, saison):
    return df[df["season"] == saison]


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
    0  John  30          180            75 1  Jane  28          165
    60 ```
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


def convertir_int(df, col):
    return df[col].astype(int)
