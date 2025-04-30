from project.view.abstract_view import AbstractView
from InquirerPy import prompt


class Q2View(AbstractView):

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu Q2",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Lancer la question 2: classement des cartons jaunes",
                    "Lancer la question 2: classement des cartons rouges",
                    "Lancer la question 2: classement des buteurs",
                    "Lancer la question 2: classement des passeurs",
                    "Retourner au menu principal",
                    "Quitter l'appli",
                ],
            }
        ]
        self.question_saison = [
            {
                "type": "list",
                "name": "question saison",
                "message": """Pour quelle saison souhaitez-vous afficher le
                "classement ?""",
                "choices": [
                    "2008/2009",
                    "2009/2010",
                    "2010/2011",
                    "2011/2012",
                    "2012/2013",
                    "2013/2014",
                    "2014/2015",
                    "2015/2016",
                ],
            }
        ]

    def make_choice(self):
        answers = prompt(self.questions)

        if (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des cartons jaunes"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q2_cartons_jaunes import run_q2a

            run_q2a(saison)
            next_view = Q2View()  # On revient au menu

        elif (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des cartons rouges"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q2_cartons_rouges import run_q2b

            run_q2b(saison)
            next_view = Q2View()  # On revient au menu

        elif (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des buteurs"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q2_meilleurs_buteurs import run_q2c

            run_q2c(saison)
            next_view = Q2View()  # On revient au menu

        elif (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des passeurs"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q2_meilleurs_passeurs import run_q2d

            run_q2d(saison)
            next_view = Q2View()  # On revient au menu

        elif answers["Menu Q2"] == "Retourner au menu principal":
            from project.view.accueil_view import AccueilView

            return AccueilView()  # On revient au menu principal

        elif answers["Menu Q2"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(" MENU Question 2".center(80, "="))
