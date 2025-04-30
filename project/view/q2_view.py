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
                    "Quitter l'appli",
                ],
            }
        ]

    def make_choice(self):
        answers = prompt(self.questions)

        if (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des cartons jaunes"
        ):
            from project.src.Q2_cartons_jaunes import run_q2a

            run_q2a()
            next_view = Q2View()  # On revient au menu

        elif (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des cartons rouges"
        ):
            from project.src.Q2_cartons_rouges import run_q2b

            run_q2b()
            next_view = Q2View()  # On revient au menu

        elif (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des buteurs"
        ):
            from project.src.Q2_meilleurs_buteurs import run_q2c

            run_q2c()
            next_view = Q2View()  # On revient au menu

        elif (
            answers["Menu Q2"]
            == "Lancer la question 2: classement des passeurs"
        ):
            from project.src.Q2_meilleurs_passeurs import run_q2d

            run_q2d()
            next_view = Q2View()  # On revient au menu

    def display_info(self):
        print(" MENU Question 2".center(80, "="))
