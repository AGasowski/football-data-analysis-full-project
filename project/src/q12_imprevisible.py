"""
Script pour identifier et afficher les matchs "surprises" (cote >= 10) selon
les bookmakers B365 et BW, avec date, score et équipes.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.manipulations import name_team_dic
from project.src.fonctions.dates_formats import formater_date_fr, date_francais
from project.src.fonctions.utils import tri_bet


def run_q12():
    """
    Retourne les 10 matchs qui ont eu les résultats les plus imprévisibles.
    """
    # Chargement des noms d'équipes
    team_names = charger_csv(
        "data/Team.csv", "dict", "team_api_id", ("team_long_name")
    )

    # Lecture des données de matchs
    matches = charger_csv(
        "data/Match.csv",
        "dict",
        "match_api_id",
        "home_team_goal",
        "away_team_goal",
        "B365H",
        "B365D",
        "B365A",
        "BWH",
        "BWD",
        "BWA",
        "home_team_api_id",
        "away_team_api_id",
        "date",
    )

    surprises_b365 = []
    surprises_bw = []

    for match in matches.values():
        try:
            home_goals = int(match[0])
            away_goals = int(match[1])
            date = match[10]
            home_team_id = match[8]
            away_team_id = match[9]

            # Déterminer le résultat
            if home_goals > away_goals:
                cote_b365 = match[2]
                cote_bw = match[5]
            elif home_goals < away_goals:
                cote_b365 = match[4]
                cote_bw = match[7]
            else:
                cote_b365 = match[3]
                cote_bw = match[6]

            # Vérification des cotes (présentes et >= 10)
            if cote_b365 and float(cote_b365) >= 10:
                surprises_b365.append(
                    {
                        "date": date,
                        "home_team": home_team_id,
                        "away_team": away_team_id,
                        "score": f"{home_goals} - {away_goals}",
                        "Cote_VainqueurB365": float(cote_b365),
                    }
                )
            if cote_bw and float(cote_bw) >= 10:
                surprises_bw.append(
                    {
                        "date": date,
                        "home_team": home_team_id,
                        "away_team": away_team_id,
                        "score": f"{home_goals} - {away_goals}",
                        "Cote_VainqueurBW": float(cote_bw),
                    }
                )
        except (ValueError, TypeError):
            continue  # Ignore les lignes invalides

    date_francais()

    surprises_b365_triees = tri_bet(surprises_b365)

    # Affichage aligné avec une largeur ajustée pour la colonne "Score"
    print("=" * 100)
    print("                       Matchs avec surprises (Bet365 ≥ 10.0)")
    print("=" * 100)
    print(f"{'Date':<30}{'Score':<55}{'Cote B365':>10}")
    print("-" * 100)

    for surprise in surprises_b365_triees[:10]:
        home_id = surprise["home_team"]
        away_id = surprise["away_team"]
        home_name = name_team_dic(team_names, home_id)
        away_name = name_team_dic(team_names, away_id)
        score_str = f"{home_name} {surprise['score']} {away_name}"
        date_str = formater_date_fr(surprise["date"])
        print(
            f"{date_str:<30}{score_str:<55}"
            f"{surprise['Cote_VainqueurB365']:>10.2f}"
        )
