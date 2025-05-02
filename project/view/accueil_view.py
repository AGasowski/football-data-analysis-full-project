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
                "message": "Pour quelle saison souhaitez-vous répondre à la "
                + "question ?",
                "choices": [
                    "Toutes les saisons réunies",
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
        self.question_saison_unique = [
            {
                "type": "list",
                "name": "question saison",
                "message": "Pour quelle saison souhaitez-vous répondre à la "
                + "question ?",
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
        self.question_championnat = [
            {
                "type": "list",
                "name": "question championnat",
                "message": "Pour quel championnat souhaitez-vous répondre "
                + "à la question ?",
                "choices": [
                    "Tous les championnats réunis",
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
        self.question_championnat_unique = [
            {
                "type": "list",
                "name": "question championnat",
                "message": "Pour quel championnat souhaitez-vous répondre "
                + "à la question ?",
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
            saison = prompt(self.question_saison_unique)["question saison"]
            champ = prompt(self.question_championnat_unique)[
                "question championnat"
            ]
            from project.src.q1_classement import run_q1

            run_q1(saison, champ)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 2":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q2_diff_buts_max import run_q2

            run_q2(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 3":
            saison = prompt(self.question_saison)["question saison"]
            if saison == "Toutes les saisons réunies":
                saison = "0"
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q3_taille_moyenne import run_q3

            run_q3(saison, champ)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 4":
            from project.view.q4_view import Q4View

            next_view = Q4View()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 5":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q5_meilleur_formation import run_q5

            run_q5(saison)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 6":
            from project.src.q6_jour_matchs_nuls import run_q6

            run_q6()
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 7":
            from project.view.q7_view import Q7View

            next_view = Q7View()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 9":
            saison = prompt(self.question_saison)["question saison"]
            if saison == "Toutes les saisons réunies":
                saison = "0"
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q9_equipe_but_exterieur import run_q9

            run_q9(saison, champ)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Lancer la question 11":
            saison = prompt(self.question_saison)["question saison"]
            if saison == "Toutes les saisons réunies":
                saison = "0"
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q11_pire_ratio_tirs import run_q11

            run_q11(saison, champ)
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Quitter l'appli":
            next_view = None

        else:
            next_view = AccueilView()

        return next_view

    def display_info(self):
        print(" MAIN MENU ".center(80, "="))
