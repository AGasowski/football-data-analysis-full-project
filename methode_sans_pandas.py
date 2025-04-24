import csv
import pandas as pd
import xml.etree.ElementTree as ET
from collections import defaultdict

# ----------------------------- ÉQUIPES ET CLASSEMENT -----------------------------


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


# ----------------------------- TRANSFORMATION XML -----------------------------


def transforme_xml_vers_dataframe(xml_string):
    """
    Transforme une chaîne XML contenant des infos de match (colonne 'goal') en DataFrame.
    """
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError:
        return pd.DataFrame()  # Retourne un DataFrame vide en cas d’erreur

    data = []
    for value in root.findall("value"):
        entry = {child.tag: child.text for child in value if child.tag != "stats"}
        stats = value.find("stats")
        if stats is not None:
            entry.update({f"stats_{child.tag}": child.text for child in stats})
        data.append(entry)
    return pd.DataFrame(data)


def top_joueurs_par_stat(chemin_match, chemin_joueurs, saison, colonne, top_n=30):
    """
    Retourne le top N des joueurs selon une statistique donnée (but ou passe).

    Args:
        chemin_match (str): Chemin vers le fichier Match.csv
        chemin_joueurs (str): Chemin vers le fichier Player.csv
        saison (str): Saison au format "YYYY/YYYY"
        colonne (str): "player1" pour les buteurs, "player2" pour les passeurs
        top_n (int): Nombre de joueurs à afficher

    Returns:
        DataFrame: Classement des joueurs
    """
    match = pd.read_csv(chemin_match)
    joueurs = pd.read_csv(chemin_joueurs)

    match = match[match["goal"].notna() & (match["goal"] != "")]
    match = match[match["season"] == saison]

    liste_actions = [transforme_xml_vers_dataframe(x) for x in match["goal"]]
    compteur = defaultdict(int)

    for df in liste_actions:
        if colonne in df.columns:
            for pid in df[colonne]:
                compteur[pid] += 1

    joueurs["player_api_id"] = joueurs["player_api_id"].astype(str)
    mapping_noms = dict(zip(joueurs["player_api_id"], joueurs["player_name"]))

    classement = [
        (mapping_noms.get(str(pid), f"ID {pid}"), nb) for pid, nb in compteur.items()
    ]
    classement = sorted(classement, key=lambda x: x[1], reverse=True)[:top_n]

    nom_colonne = "Buts marqués" if colonne == "player1" else "Passes décisives"
    return pd.DataFrame(classement, columns=["Nom du joueur", nom_colonne])
