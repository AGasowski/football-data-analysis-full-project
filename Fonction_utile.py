import csv
import pandas as pd
import xml.etree.ElementTree as ET
from collections import defaultdict


def charger_noms_equipes(chemin_fichier):
    """Charge les noms des équipes à partir d’un fichier CSV."""
    noms_equipes = {}
    with open(chemin_fichier, mode="r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            id_equipe = int(ligne["team_api_id"])
            nom_equipe = ligne["team_long_name"]
            noms_equipes[id_equipe] = nom_equipe
    return noms_equipes


def calculer_statistiques_equipes(chemin_matchs, noms_equipes, id_ligue, saison):
    """Calcule les statistiques (points, buts marqués/encaissés) pour chaque équipe."""
    stats = defaultdict(lambda: {"points": 0, "marqués": 0, "encaissés": 0})
    with open(chemin_matchs, mode="r", encoding="utf-8") as fichier:
        lecteur = csv.DictReader(fichier)
        for ligne in lecteur:
            if int(ligne["league_id"]) == id_ligue and ligne["season"] == saison:
                id_domicile = int(ligne["home_team_api_id"])
                id_exterieur = int(ligne["away_team_api_id"])
                buts_domicile = int(ligne["home_team_goal"])
                buts_exterieur = int(ligne["away_team_goal"])

                stats[id_domicile]["marqués"] += buts_domicile
                stats[id_domicile]["encaissés"] += buts_exterieur
                stats[id_exterieur]["marqués"] += buts_exterieur
                stats[id_exterieur]["encaissés"] += buts_domicile

                if buts_domicile > buts_exterieur:
                    stats[id_domicile]["points"] += 3
                elif buts_domicile < buts_exterieur:
                    stats[id_exterieur]["points"] += 3
                else:
                    stats[id_domicile]["points"] += 1
                    stats[id_exterieur]["points"] += 1
    return stats


def generer_classement(stats, noms_equipes):
    """Génère un classement basé sur les statistiques des équipes."""
    classement = []
    for id_equipe, donnees in stats.items():
        nom = noms_equipes.get(id_equipe, f"Équipe {id_equipe}")
        difference_buts = donnees["marqués"] - donnees["encaissés"]
        classement.append(
            (
                nom,
                donnees["points"],
                donnees["marqués"],
                donnees["encaissés"],
                difference_buts,
            )
        )
    classement.sort(key=lambda x: (x[1], x[4], x[2]), reverse=True)
    return classement
