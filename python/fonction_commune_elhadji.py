import csv
def filtrer_match_csv(chemin, conditions, colonnes_a_garder):
    """
    Filtre un fichier CSV selon des conditions personnalisées et retourne un dictionnaire
    dont les valeurs sont des listes des colonnes spécifiées.

    Paramètres
    ----------
    chemin : str
        Chemin d'accès au fichier CSV.
    conditions : dict
        Dictionnaire de conditions : {nom_colonne: condition (str ou fonction)}.
        Exemple :
            {"season": "2014/2015", "league_id": "21518", "shoton": lambda x: x != ""}
    colonnes_a_garder : list
        Liste des colonnes à extraire pour chaque ligne valide.

    Retour
    ------
    dict
        Dictionnaire {match_api_id: [val1, val2, val3, ...]} pour les colonnes spécifiées.
    """
    match_dict = {}
    
    with open(chemin, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            valide = True
            for col, cond in conditions.items():
                valeur = row[col]
                if callable(cond):
                    if not cond(valeur):
                        valide = False
                        break
                else:
                    if valeur != cond:
                        valide = False
                        break

            if valide:
                match_id = int(row["match_api_id"])
                valeurs = [row[col] for col in colonnes_a_garder]
                match_dict[match_id] = valeurs
    
    return match_dict

def compter_lignes_par_team(table, id_team):
    """
    Compte le nombre de lignes dans une table où la colonne 'team' correspond à un identifiant donné.

    Paramètres
    ----------
    table : list of dict
        Une table représentée sous forme de liste de dictionnaires (chaque dictionnaire = une ligne).
    id_team : str or int
        L'identifiant de l'équipe à chercher dans la colonne 'team'.

    Retour
    ------
    int
        Le nombre de lignes où table[i]['team'] == id_team.
        Si la colonne 'team' n'existe pas, retourne 1 par défaut.
    """
    if  "team" not in table.columns:
        return 1

    return sum(1 for ligne in table if ligne[("team")] == int(id_team)) 

import xml.etree.ElementTree as ET
import csv

import xml.etree.ElementTree as ET
import csv

def transforme(X, chemin_csv):
    """
    Convertit un code XML en fichier CSV.

    Paramètres:
    -----------
    X : str
        Une chaîne de caractères contenant un document XML.
    chemin_csv : str
        Le chemin où enregistrer le fichier CSV.

    Exemples:
    ---------
    ```python
    xml_data = '''<root>
        <value>
            <name>John</name> <age>30</age> <stats>
                <height>180</height> <weight>75</weight>
            </stats>
        </value> 
        <value>
            <name>Jane</name> <age>28</age> <stats>
                <height>165</height> <weight>60</weight>
            </stats>
        </value>
    </root>'''

    transforme(xml_data, 'output.csv')
    ```

    Cela générera un fichier CSV `output.csv` avec les données extraites du XML.
    """
    root = ET.fromstring(X)
    data = []
    header = set()  # Utiliser un set pour éviter les doublons
    
    # Extraction des données du XML
    for value in root.findall("value"):
        entry = {
            child.tag: child.text for child in value if child.tag != "stats"
        }  # Exclure "stats" pour l'instant
        stats = value.find("stats")  # Extraire les stats
        if stats is not None:
            entry.update({f"stats_{child.tag}": child.text for child in stats})
            data.append(entry)
            
            # Ajouter les clés du dictionnaire à l'en-tête
            header.update(entry.keys())
    
    # Convertir le header en une liste (pour DictWriter)
    header = list(header)
    
    # Écrire les données dans le fichier CSV
    with open(chemin_csv, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()  # Écrire les en-têtes
        writer.writerows(data)  # Écrire les lignes
