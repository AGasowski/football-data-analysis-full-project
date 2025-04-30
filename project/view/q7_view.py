from project.view.abstract_view import AbstractView
from InquirerPy import prompt


class Q7View(AbstractView):

    def __init__(self):
        super().__init__()
        self.answers = [
            {
                "type": "list",
                "name": "Menu Q7",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Equipe type général (entre 2008 et 2016)",
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
        answers = prompt(self.answers)

        if answers["Menu Q7"] == "Equipe type général (entre 2008 et 2016)":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("0")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2008/2009":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2008/2009")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2009/2010":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2009/2010")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2010/2011":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2010/2011")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2011/2012":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2011/2012")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2012/2013":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2012/2013")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2013/2014":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2013/2014")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2014/2015":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2014/2015")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Equipe type 2015/2016":

            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7("2015/2016")
            next_view = Q7View()  # On revient au menu

        elif answers["Menu Q7"] == "Retourner au menu principal":
            from project.view.accueil_view import AccueilView

            return AccueilView()  # On revient au menu principal

        elif answers["Menu Q7"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(" MENU Question 2".center(80, "="))
