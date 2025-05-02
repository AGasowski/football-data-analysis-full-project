from project.view.abstract_view import AbstractView
from InquirerPy import prompt


class Q4View(AbstractView):

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu Q4",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Lancer la question 4: classement des cartons jaunes",
                    "Lancer la question 4: classement des cartons rouges",
                    "Lancer la question 4: classement des buteurs",
                    "Lancer la question 4: classement des passeurs",
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
            answers["Menu Q4"]
            == "Lancer la question 4: classement des cartons jaunes"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q4_cartons_jaunes import run_q4a

            run_q4a(saison)
            next_view = Q4View()  # On revient au menu

        elif (
            answers["Menu Q4"]
            == "Lancer la question 4: classement des cartons rouges"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q4_cartons_rouges import run_q4b

            run_q4b(saison)
            next_view = Q4View()  # On revient au menu

        elif (
            answers["Menu Q4"]
            == "Lancer la question 4: classement des buteurs"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q4_meilleurs_buteurs import run_q4c

            run_q4c(saison)
            next_view = Q4View()  # On revient au menu

        elif (
            answers["Menu Q4"]
            == "Lancer la question 4: classement des passeurs"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q4_meilleurs_passeurs import run_q4d

            run_q4d(saison)
            next_view = Q4View()  # On revient au menu

        elif answers["Menu Q4"] == "Retourner au menu principal":
            from project.view.accueil_view import AccueilView

            return AccueilView()  # On revient au menu principal

        elif answers["Menu Q4"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(" MENU Question 4".center(80, "="))
