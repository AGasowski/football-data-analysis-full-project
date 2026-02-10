"""
Module AppView

Ce module définit la classe `AppView`, une vue interactive permettant de
prédire le classement final d'une équipe sportive, soit avant le début de la
saison, soit à la mi-saison, en utilisant des méthodes d'apprentissage
automatique.
"""

from InquirerPy import prompt
import pandas as pd
from view.abstract_view import AbstractView
from src.fonctions.names import championnat, get_equipes_participantes


class AppView(AbstractView):
    """
    Classe AppView - Interface de prédiction de classements sportifs

    La classe AppView permet à l'utilisateur de prévoir le classement final
    d'une équipe de football, en choisissant la saison, le championnat,
    l'équipe et la méthode de prédiction. Les méthodes d'apprentissage
    automatique disponibles sont la régression linéaire et le modèle de
    Poisson.

    Attributs :
    ----------
    questions : list
        Liste de dictionnaires contenant les choix du menu principal.
    question_meth : list
        Liste de dictionnaires pour sélectionner la méthode de prédiction.
    question_saison : list
        Liste de dictionnaires pour sélectionner la saison.
    question_equipe : list
        Liste de dictionnaires pour sélectionner l'équipe.
    question_championnat : list
        Liste de dictionnaires pour sélectionner le championnat.

    Méthodes :
    ---------
    make_choice()
        Affiche le menu principal et gère les choix de l'utilisateur pour
        prédire les classements ou revenir au menu principal.
    display_info()
        Affiche le titre du menu d'apprentissage automatique.
    """

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu Apprentissage",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Prévoir le classement final d'une équipe avant le "
                    "début de la saison",
                    "Prévoir le classement final d'une équipe à la "
                    "mi-saison",
                    "Retourner au menu principal",
                    "Quitter l'appli",
                ],
            }
        ]
        self.question_meth = [
            {
                "type": "list",
                "name": "question méthode",
                "message": "Quelle méthode souhaitez-vous utiliser ?",
                "choices": ["Méthode linéaire", "Méthode de Poisson"],
            }
        ]
        self.question_saison = [
            {
                "type": "list",
                "name": "question saison",
                "message": "Pour quelle saison souhaitez-vous afficher le "
                "classement ?",
                "choices": [
                    "2014/2015",
                    "2015/2016",
                ],
            }
        ]
        self.question_equipe = [
            {
                "type": "list",
                "name": "question équipe",
                "message": "Quelle équipe souhaitez-vous sélectionner ?",
                "choices": [],
            }
        ]
        self.question_championnat = [
            {
                "type": "list",
                "name": "question champ",
                "message": "Pour quel championnat souhaitez-vous répondre "
                "à la question ?",
                "choices": [
                    "Ligue 1 (France)",
                    "Premier League (Angleterre)",
                    "Bundesliga (Allemagne)",
                    "Serie A (Italie)",
                    "Liga BBVA (Espagne)",
                    "Eredivisie (Pays-Bas)",
                    "Liga ZON Sagres (Portugal)",
                    "Ekstraklasa (Pologne)",
                    "Jupiler League (Belgique)",
                    "Super League (Suisse)",
                ],
            }
        ]

    def make_choice(self):
        next_view = None
        answers = prompt(self.questions)

        if (
            answers["Menu Apprentissage"]
            == "Prévoir le classement final d'une équipe avant le début de "
            "la saison"
        ):
            meth = prompt(self.question_meth)["question méthode"]
            saison = prompt(self.question_saison)["question saison"]
            champ = prompt(self.question_championnat)["question champ"]
            id_champ = championnat(champ)

            # Obtenir la liste des équipes participantes
            equipes = get_equipes_participantes(champ, saison)

            # Poser la question à l'utilisateur
            question_equipe = [
                {
                    "type": "list",
                    "name": "question_equipe",
                    "message": "Quelle équipe souhaitez-vous "
                    "sélectionner ?",
                    "choices": equipes,
                }
            ]
            equipe = prompt(question_equipe)["question_equipe"]

            # Charger les données des équipes
            teams_df = pd.read_csv("data/Team.csv")

            # Obtenir l'ID de l'équipe sélectionnée
            id_team = teams_df[teams_df["team_long_name"] == equipe][
                "team_api_id"
            ].values[0]
            if meth == "Méthode linéaire":
                from src.Apprentissage1_lineaire import (
                    predire_classement_avec_confiance,
                )

                predire_classement_avec_confiance(saison, id_champ, id_team)

                next_view = AppView()
            elif meth == "Méthode de Poisson":
                from src.Apprentissage1_poisson import (
                    predire_classement_avec_confiance,
                )

                predire_classement_avec_confiance(saison, id_champ, id_team)

                next_view = AppView()

        elif (
            answers["Menu Apprentissage"]
            == "Prévoir le classement final d'une équipe à la mi-saison"
        ):
            saison = prompt(self.question_saison)["question saison"]
            champ = prompt(self.question_championnat)["question champ"]
            id_champ = championnat(champ)

            # Obtenir la liste des équipes participantes
            equipes = get_equipes_participantes(champ, saison)

            # Poser la question à l'utilisateur
            question_equipe = [
                {
                    "type": "list",
                    "name": "question_equipe",
                    "message": "Quelle équipe souhaitez-vous "
                    "sélectionner ?",
                    "choices": equipes,
                }
            ]
            equipe = prompt(question_equipe)["question_equipe"]

            # Charger les données des équipes
            teams_df = pd.read_csv("data/Team.csv")

            # Obtenir l'ID de l'équipe sélectionnée
            id_team = teams_df[teams_df["team_long_name"] == equipe][
                "team_api_id"
            ].values[0]
            from src.Apprentissage2_poisson import (
                predire_classement_avec_confiance,
            )

            predire_classement_avec_confiance(saison, id_champ, id_team)

            next_view = AppView()  # On revient au menu principal

        elif answers["Menu Apprentissage"] == "Retourner au menu principal":
            from view.accueil_view import AccueilView

            next_view = AccueilView()  # On revient au menu principal

        elif answers["Menu Apprentissage"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(" MENU Apprentissage automatique ".center(100, "="))
