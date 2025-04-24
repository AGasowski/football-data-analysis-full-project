import tkinter as tk
from tkinter import ttk
from methode_sans_pandas import (
    charger_noms_equipes,
    calculer_statistiques_equipes,
    generer_classement,
)

# Chargement des noms des équipes depuis le fichier CSV
noms_equipes = charger_noms_equipes("data/Team.csv")

# Calcul des statistiques pour la saison 2014/2015 de la Premier League (id_ligue = 1729)
statistiques = calculer_statistiques_equipes(
    "data/Match.csv", noms_equipes, id_ligue=1729, saison="2014/2015"
)

# Génération du classement final
classement = generer_classement(statistiques, noms_equipes)

# Affichage du classement dans la console
print("Classement de la saison 2014/2015 :")
print(
    "{:<25} {:<10} {:<10} {:<10} {:<10}".format(
        "Équipe", "Points", "Marqués", "Encaissés", "Différence"
    )
)
for equipe, points, marques, encaisses, difference in classement:
    print(f"{equipe:<25} {points:<10} {marques:<10} {encaisses:<10} {difference:<10}")

# Création de la fenêtre principale avec Tkinter
fenetre = tk.Tk()
fenetre.title("Classement Premier League 2014/2015")
fenetre.geometry("600x400")
fenetre.configure(bg="#2C3E50")

# Cadre pour contenir le tableau
cadre = tk.Frame(fenetre, bg="#2C3E50")
cadre.pack(pady=20)

# Définition des colonnes du tableau
colonnes = ("Équipe", "Points", "Marqués", "Encaissés", "Différence")
tableau = ttk.Treeview(cadre, columns=colonnes, show="headings")

# Configuration des colonnes
for colonne in colonnes:
    tableau.heading(colonne, text=colonne, anchor="center")
    tableau.column(colonne, anchor="center")

# Insertion des données dans le tableau
for equipe, points, marques, encaisses, difference in classement:
    tableau.insert("", tk.END, values=(equipe, points, marques, encaisses, difference))

# Affichage du tableau
tableau.pack()

# Bouton pour fermer la fenêtre
bouton_fermer = tk.Button(
    fenetre,
    text="Fermer",
    command=fenetre.quit,
    bg="#E74C3C",
    fg="white",
    font=("Arial", 12, "bold"),
)
bouton_fermer.pack(pady=10)

# Lancement de la boucle principale Tkinter
fenetre.mainloop()
