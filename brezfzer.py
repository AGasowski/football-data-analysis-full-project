import csv
from collections import defaultdict
import tkinter as tk
from tkinter import ttk 

# Dictionnaire pour stocker les noms des équipes
team_names = {}
match={}
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
        tir_cadre = (row["shoton"])
        id_domicile=int(row["home_team_api_id"])
        id_exterieur=int(row["away_team_api_id"])
        but_domicile=(row["home_team_goal"])
        but_exterieur=row["away_team_goal"]
        match[match_id] =[id_domicile,id_exterieur,but_domicile,but_exterieur,tir_cadre]

print(match)

