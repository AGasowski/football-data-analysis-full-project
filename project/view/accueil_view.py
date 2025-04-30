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
                    "Lancer la question 6",
                    "Lancer la question 7",
                    "Lancer la question 9",
                    "Quitter l'appli",
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
            from project.src.Q1_classement_PL import run_q1

            run_q1()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 3":
            from project.src.Q3_taille_moyenne import run_q3

            run_q3()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 4":
            from project.src.Q4_diff_buts_max import run_q4

            run_q4()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 5":
            from project.src.Q5_meilleur_formation import run_q5

            run_q5()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 6":
            from project.src.Q6_jour_matchs_nuls import run_q6

            run_q6()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 7":
            from project.src.Q7_equipe_type_affichage import run_q7

            run_q7()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 9":
            from project.src.Q9_equipe_but_exterieur import run_q9

            run_q9()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Quitter l'appli":
            next_view = None

        else:
            next_view = AccueilView()

        return next_view

    def display_info(self):
        print(" MAIN MENU ".center(80, "="))
