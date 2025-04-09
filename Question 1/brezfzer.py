import csv
from collections import defaultdict
import tkinter as tk
from tkinter import ttk 

# Dictionnaire pour stocker les noms des équipes
team_names = {}

# Chargement des noms des équipes
with open("data/Team.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_id = int(row["team_api_id"])
        team_name = row["team_long_name"]
        team_names[team_id] = team_name
print(team_names) 
