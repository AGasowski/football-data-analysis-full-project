from project.view.abstract_view import AbstractView
from InquirerPy import prompt


class AccueilView(AbstractView):

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "S'identifier en tant qu'admin",
                    "S'identifier en tant qu'utilisateur",
                    "Lancer la question 1",
                    "Lancer la question 2",
                    "Lancer la question 3",
                    "Lancer la question 4",
                    "Lancer la question 5",
                    "Lancer la question 6",
                    "Lancer la question 7",
                    "Lancer la question 9",
                    "Lancer la question 11",
                    "Quitter l'appli",
                ],
            }
        ]
        self.question_saison = [
            {
                "type": "list",
                "name": "question saison",
                "message": """Pour quelle saison souhaitez-vous répondre à la
                           question ?""",
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

        if answers["Menu principal"] == "S'identifier en tant qu'admin":
            from project.view.admin_view import AdminView

            next_view = AdminView()

        elif (
            answers["Menu principal"] == "S'identifier en tant qu'utilisateur"
        ):
            from project.view.user_view import UserView

            next_view = UserView()

        elif answers["Menu principal"] == "Lancer la question 1":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q1_classement_PL import run_q1

            run_q1(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 2":
            from project.view.q2_view import Q2View

            next_view = Q2View()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 3":
            from project.src.Q3_taille_moyenne import run_q3

            run_q3()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 4":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q4_diff_buts_max import run_q4

            run_q4(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 5":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q5_meilleur_formation import run_q5

            run_q5(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 6":
            from project.src.Q6_jour_matchs_nuls import run_q6

            run_q6()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 7":
            from project.view.q7_view import Q7View

            next_view = Q7View()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 9":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q9_equipe_but_exterieur import run_q9

            run_q9(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 11":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            from project.src.Q11_pire_ratio_tirs import run_q11

            run_q11(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Quitter l'appli":
            next_view = None

        else:
            next_view = AccueilView()

        return next_view

    def display_info(self):
        print(" MAIN MENU ".center(80, "="))
