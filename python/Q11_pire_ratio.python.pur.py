
from fonction_commune_elhadji import (filtrer_match_csv,compter_lignes_par_team,transforme) 

import csv


conditions = {
    "season": "2014/2015",
    "league_id": "21518",
    "shoton": lambda x: x.strip() != "",
    "goal": lambda x: x.strip() != "" 
}

colonnes_a_garder = ["goal","shoton","home_team_api_id"]

d= filtrer_match_csv("data/Match.csv", conditions, colonnes_a_garder)
#print(d)
def ajouter_xml_dans_csv(d, chemin_csv):
    """
    Ajoute plusieurs fichiers XML (extraits du dictionnaire d) dans un fichier CSV.
    
    Paramètres:
    ----------
    d : dict
        Dictionnaire contenant les éléments XML sous forme de chaîne.
    chemin_csv : str
        Chemin du fichier CSV dans lequel les résultats doivent être ajoutés.
    """
    for key in d:
        xml_data = d[key]  # Obtenir l'élément XML
        df = transforme(xml_data)  # Transformer l'élément XML en DataFrame

        # Ajouter les données au fichier CSV
        df.to_csv(chemin_csv, mode='a', header=not os.path.exists(chemin_csv), index=False)

L={}
for e in d:
    if d[e][2] not in L:
        L[d[e][2]] = []
    else:
        L[d[e][2]].append(compter_lignes_par_team(d[e][0],d[e][2])/(compter_lignes_par_team(d[e][0],d[e][2])+compter_lignes_par_team(d[e][1],d[e][2]))) 
print(L)