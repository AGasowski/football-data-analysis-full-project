import pandas as pd
import xml.etree.ElementTree as ET


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
        Un DataFrame contenant les données extraites du XML, avec les attributs des éléments "value"
        comme colonnes et les sous-éléments de "stats" préfixés par "stats_".

    Exemples:
    ---------
    ```python
    xml_data = \"\"\"<root>
        <value>
            <name>John</name>
            <age>30</age>
            <stats>
                <height>180</height>
                <weight>75</weight>
            </stats>
        </value>
        <value>
            <name>Jane</name>
            <age>28</age>
            <stats>
                <height>165</height>
                <weight>60</weight>
            </stats>
        </value>
    </root>\"\"\"

    df = transforme(xml_data)
    print(df)
    ```
    Résultat :
    ```
       name age  stats_height  stats_weight
    0  John  30          180            75
    1  Jane  28          165            60
    ```
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
