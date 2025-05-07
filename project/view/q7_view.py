"""
Module Q7View - Interface pour la création du 11 type

Ce module contient la classe Q7View, qui permet de gérer l'interface
utilisateur pour la visualisation du 11 type
"""

from InquirerPy import prompt
from project.view.abstract_view import AbstractView


class Q7View(AbstractView):
    """
    Classe Q7View - Interface de visualisation du 11 type

    La classe Q7View permet d'interagir avec l'utilisateur pour afficher divers
    11 types liés aux performances sportives.
    """

    def __init__(self):
        super().__init__()
        self.question_saison = [
            {
                "type": "list",
                "name": "question saison",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Equipe type générale (entre 2008 et 2016)",
                    "Equipe type 2008/2009",
                    "Equipe type 2009/2010",
                    "Equipe type 2010/2011",
                    "Equipe type 2011/2012",
                    "Equipe type 2012/2013",
                    "Equipe type 2013/2014",
                    "Equipe type 2014/2015",
                    "Equipe type 2015/2016",
                    "Retourner au menu principal",
                    "Quitter l'appli",
                ],
            }
        ]

    def make_choice(self):
        saison = prompt(self.question_saison)["question saison"]

        if saison == "Equipe type générale (entre 2008 et 2016)":
            saison = "0"

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("0")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2008/2009":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2008/2009")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2009/2010":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2009/2010")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2010/2011":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2010/2011")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2011/2012":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2011/2012")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2012/2013":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2012/2013")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2013/2014":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2013/2014")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2014/2015":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2014/2015")
            next_view = Q7View()  # On revient au menu

        elif saison == "Equipe type 2015/2016":

            from project.src.q7_equipe_type_affichage import run_q7

            run_q7("2015/2016")
            next_view = Q7View()  # On revient au menu

        elif saison == "Retourner au menu principal":
            from project.view.accueil_view import AccueilView

            return AccueilView()  # On revient au menu principal

        elif saison == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(" MENU Question 7".center(80, "="))
