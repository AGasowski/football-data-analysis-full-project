"""
Module : accueil_view

Ce module contient la classe AccueilView qui gère
l'affichage du menu principal et la gestion des choix de l'utilisateur.
"""

from project.view.abstract_view import AbstractView
from InquirerPy import prompt
from project.src.fonctions.save import capture_et_enregistrer_png


class AccueilView(AbstractView):

    def __init__(self):
        """
        Classe représentant la vue du menu principal (Accueil) de
        l'application.

        Cette classe permet à l'utilisateur de choisir entre plusieurs options
        disponibles, telles que l'affichage de classements, des matchs, ou des
        statistiques, en fonction de la saison et du championnat sélectionnés.
        Chaque choix mène à l'exécution d'une fonction spécifique.
        """
        super().__init__()
        self.questions = [
            {
                "type": "list",
                "name": "Menu principal",
                "message": "Que souhaitez-vous faire ?",
                "choices": [
                    "Q1 - Afficher le classement d'un championnat",
                    "Q2 - Afficher les matchs avec la plus grande différence "
                    "de buts",
                    "Q3 - Afficher la taille moyenne des buteurs de tête",
                    "Q4 - Afficher un classement de statistiques",
                    "Q5 - Afficher le classement des dispositifs les plus "
                    "utilisés",
                    "Q6 - Afficher le jour qui a connu le plus de matchs nuls",
                    "Q7 - Afficher l'équipe type",
                    "Q8 - Afficher le classement des équipes avec un 11 "
                    "régulier",
                    "Q9 - Afficher le classement des équipes marquant plus "
                    "à l'extérieur",
                    "Q10 - Afficher l'évolution des aptitudes par catégorie "
                    "d'âge",
                    "Q11 - Afficher l'équipe ayant le pire ratio de buts/tirs "
                    "cadrés",
                    "Q12 - Afficher le classement des matchs les plus "
                    "imprévisibles",
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
        self.question_championnat_unique = [
            {
                "type": "list",
                "name": "question championnat",
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
        answers = prompt(self.questions)

        if (
            answers["Menu principal"]
            == "Q1 - Afficher le classement d'un championnat"
        ):
            saison = prompt(self.question_saison_unique)["question saison"]
            saison_clean = saison.replace("/", "_")
            champ = prompt(self.question_championnat_unique)[
                "question championnat"
            ]
            from project.src.q1_classement import run_q1

            capture_et_enregistrer_png(
                run_q1,
                saison,
                champ,
                chemin=f"output/classement_{champ}_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q2 - Afficher les matchs avec la plus grande différence de "
            "buts"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q2_diff_buts_max import run_q2

            capture_et_enregistrer_png(
                run_q2,
                saison,
                chemin=f"output/diff_buts_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q3 - Afficher la taille moyenne des buteurs de tête"
        ):
            saison = prompt(self.question_saison)["question saison"]
            saison_clean = saison.replace("/", "_")
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q3_taille_moyenne import run_q3

            capture_et_enregistrer_png(
                run_q3,
                saison,
                chemin=f"output/taille_buts_tete_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q4 - Afficher un classement de statistiques"
        ):
            from project.view.q4_view import Q4View

            next_view = Q4View()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q5 - Afficher le classement des dispositifs les plus "
            "utilisés"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q5_meilleur_formation import run_q5

            capture_et_enregistrer_png(
                run_q5,
                saison,
                chemin=f"output/formations_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q6 - Afficher le jour qui a connu le plus de matchs nuls"
        ):
            answersaison = prompt(self.question_saison)
            saison = answersaison["question saison"]
            saison_clean = saison.replace("/", "_")
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q6_jour_matchs_nuls import run_q6

            capture_et_enregistrer_png(
                run_q6,
                saison,
                chemin=f"output/matchs_nuls_max_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Q7 - Afficher l'équipe type":
            from project.view.q7_view import Q7View

            next_view = Q7View()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q8 - Afficher le classement des équipes avec un 11 régulier"
        ):
            from project.src.q8_variance_11 import run_q8

            capture_et_enregistrer_png(
                run_q8,
                chemin="output/coherence.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q9 - Afficher le classement des équipes marquant plus à "
            "l'extérieur"
        ):
            saison = prompt(self.question_saison)["question saison"]
            saison_clean = saison.replace("/", "_")
            if saison == "Toutes les saisons réunies":
                saison = "0"
            from project.src.q9_equipe_but_exterieur import run_q9

            capture_et_enregistrer_png(
                run_q9,
                saison,
                chemin=f"output/equipes_exterieur_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q10 - Afficher l'évolution des aptitudes par catégorie d'âge"
        ):
            from project.src.q10_aptitudes_age import run_q10

            run_q10()
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q11 - Afficher l'équipe ayant le pire ratio de buts/tirs "
            "cadrés"
        ):
            saison = prompt(self.question_saison)["question saison"]
            saison_clean = saison.replace("/", "_")
            if saison == "Toutes les saisons réunies":
                saison = "0"
            champ = prompt(self.question_championnat)["question championnat"]
            from project.src.q11_pire_ratio_tirs import run_q11

            capture_et_enregistrer_png(
                run_q11,
                saison,
                champ,
                chemin=f"output/pire_ratio_{champ}_{saison_clean}.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif (
            answers["Menu principal"]
            == "Q12 - Afficher le classement des matchs les plus imprévisibles"
        ):
            from project.src.q12_imprevisible import run_q12

            capture_et_enregistrer_png(
                run_q12,
                chemin="output/imprevisible.png",
            )
            next_view = AccueilView()  # On revient au menu

        elif answers["Menu principal"] == "Quitter l'appli":
            next_view = None

        else:
            next_view = AccueilView()

        return next_view

    def display_info(self):
        print(" MAIN MENU ".center(80, "="))
