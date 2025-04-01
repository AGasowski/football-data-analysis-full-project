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

# Dictionnaire pour stocker les statistiques des équipes
stats = defaultdict(lambda: {"points": 0, "scored": 0, "conceded": 0})

# Chargement des matchs et calcul des statistiques
with open("data/Match.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        league_id = int(row["league_id"])
        season = row["season"]

        if league_id == 1729 and season == "2014/2015":
            home_id = int(row["home_team_api_id"])
            away_id = int(row["away_team_api_id"])
            home_goals = int(row["home_team_goal"])
            away_goals = int(row["away_team_goal"])

            # Mise à jour des buts marqués et encaissés
            stats[home_id]["scored"] += home_goals
            stats[home_id]["conceded"] += away_goals
            stats[away_id]["scored"] += away_goals
            stats[away_id]["conceded"] += home_goals

            # Attribution des points
            if home_goals > away_goals:  # Victoire équipe à domicile
                stats[home_id]["points"] += 3
            elif home_goals < away_goals:  # Victoire équipe à l'extérieur
                stats[away_id]["points"] += 3
            else:  # Match nul
                stats[home_id]["points"] += 1
                stats[away_id]["points"] += 1

# Génération du classement
ranking = []
for team_id, data in stats.items():
    ranking.append(
        (
            team_names[team_id],
            data["points"],
            data["scored"],
            data["conceded"],
            data["scored"] - data["conceded"],
        )
    )

# Tri du classement : d'abord par points, puis par différence de buts, puis par buts marqués
ranking.sort(key=lambda x: (x[1], x[4], x[2]), reverse=True)

# Affichage du classement
print("Classement de la saison 2014/2015 :")
print(
    "{:<25} {:<10} {:<10} {:<10} {:<10}".format(
        "Équipe", "Points", "Marqués", "Encaissés", "Différence"
    )
)
for team, points, scored, conceded, diff in ranking:
    print(f"{team:<25} {points:<10} {scored:<10} {conceded:<10} {diff:<10}")

# Création de la fenêtre d'affichage
root = tk.Tk()
root.title("Classement Premier League 2014/2015")
root.geometry("600x400")
root.configure(bg="#2C3E50")

# Création d'un tableau avec ttk.Treeview
frame = tk.Frame(root, bg="#2C3E50")
frame.pack(pady=20)

columns = ("Équipe", "Points", "Marqués", "Encaissés", "Différence")
tree = ttk.Treeview(frame, columns=columns, show="headings")

# Définition des colonnes
for col in columns:
    tree.heading(col, text=col, anchor="center")
    tree.column(col, anchor="center")

# Ajout des données au tableau
for team, points, scored, conceded, diff in ranking:
    tree.insert("", tk.END, values=(team, points, scored, conceded, diff))

# Ajout du tableau à la fenêtre
tree.pack()

# Bouton de fermeture
button = tk.Button(
    root,
    text="Fermer",
    command=root.quit,
    bg="#E74C3C",
    fg="white",
    font=("Arial", 12, "bold"),
)
button.pack(pady=10)

# Lancement de l'interface graphique
root.mainloop()
