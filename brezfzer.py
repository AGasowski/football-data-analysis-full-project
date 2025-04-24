import csv
from collections import defaultdict
import tkinter as tk
from tkinter import ttk

# Dictionnaire pour stocker les noms des équipes
team_names = {}
match = {}
# Chargement des noms des équipes
with open("data/Team.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_id = int(row["team_api_id"])
        team_name = row["team_long_name"]
        team_names[team_id] = team_name
with open("data/Match.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        match_id = int(row["match_api_id"])
        tir_cadre = row["shoton"]
        id_domicile = int(row["home_team_api_id"])
        id_exterieur = int(row["away_team_api_id"])
        but_domicile = row["home_team_goal"]
        but_exterieur = row["away_team_goal"]
        match[match_id] = [
            id_domicile,
            id_exterieur,
            but_domicile,
            but_exterieur,
            tir_cadre,
        ]

final = {}
for equipe in team_names:
    for matchs in match:
        if equipe == match[matchs][0]:
            if team_names[equipe] not in final:
                final[team_names[equipe]] = []
            final[team_names[equipe]].append((int(match[matchs][2])+int(match[matchs][3]))/int(match[matchs][4]))                

def moyenne(L):
    cpt = 0
    for i in range(len(L)):
        cpt += L[i] / len(L)
    return cpt


for e in final:
    final[e] = moyenne(final[e])


print(final) 
