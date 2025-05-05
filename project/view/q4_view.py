from project.view.abstract_view import AbstractView
from InquirerPy import prompt
from project.src.fonctions.save import capture_et_enregistrer_png


class Q4View(AbstractView):

    def __init__(self):
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu Q4",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Q4: Classement des cartons jaunes",
                    "Q4: Classement des cartons rouges",
                    "Q4: Classement des buteurs",
                    "Q4: Classement des passeurs",
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
        self.question_championnat = [
            {
                "type": "list",
                "name": "question championnat",
                "message": "Pour quel championnat souhaitez-vous répondre "
                "à la question ?",
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

    def make_choice(self):
        answers = prompt(self.questions)

        if answers["Menu Q4"] == "Q4: Classement des cartons jaunes":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q4_stats import run_q4

            capture_et_enregistrer_png(
                run_q4,
                saison,
                champ,
                "jaune",
                chemin=f"output/classement_jaunes_{saison_clean}.png",
            )
            next_view = Q4View()  # On revient au menu

        elif answers["Menu Q4"] == "Q4: Classement des cartons rouges":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q4_stats import run_q4

            capture_et_enregistrer_png(
                run_q4,
                saison,
                champ,
                "rouge",
                chemin=f"output/classement_rouges_{saison_clean}.png",
            )
            next_view = Q4View()  # On revient au menu

        elif answers["Menu Q4"] == "Q4: Classement des buteurs":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q4_stats import run_q4

            capture_et_enregistrer_png(
                run_q4,
                saison,
                champ,
                "but",
                chemin=f"output/classement_buteurs_{saison_clean}.png",
            )
            next_view = Q4View()  # On revient au menu

        elif answers["Menu Q4"] == "Q4: Classement des passeurs":
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q4_stats import run_q4

            capture_et_enregistrer_png(
                run_q4,
                saison,
                champ,
                "passe",
                chemin=f"output/classement_passeurs_{saison_clean}.png",
            )
            next_view = Q4View()  # On revient au menu

        elif answers["Menu Q4"] == "Retourner au menu principal":
            from project.view.accueil_view import AccueilView

            return AccueilView()  # On revient au menu principal

        elif answers["Menu Q4"] == "Quitter l'appli":
            next_view = None

        return next_view

    def display_info(self):
        print(" MENU Question 4".center(80, "="))
