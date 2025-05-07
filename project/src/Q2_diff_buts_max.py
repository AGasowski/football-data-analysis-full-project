"""
Script pour afficher le match avec le plus grand écart de buts pour une
saison donnée.
"""

from project.src.fonctions.data_loader import charger_csv
from project.src.fonctions.manipulations import (
    id_championnat,
)


def run_q2(saison, league):
    """
    Affiche le match avec le plus grand écart de buts pour une saison donnée.

    Args:
        saison (str): Saison ciblée au format "2014/2015". Si "0", utilise
        toutes les saisons.
    """
    print("=" * 56)
    print("    Matchs avec la plus grande différence de buts")
    print("=" * 56)
    teams = charger_csv(
        "data/Team.csv", "dict", "team_api_id", "team_long_name"
    )
    matchs = charger_csv(
        "data/Match.csv",
        "dict",
        "id",
        "season",
        "league_id",
        "home_team_api_id",
        "away_team_api_id",
        "home_team_goal",
        "away_team_goal",
    )

    league_id = id_championnat(league)

    max_diff = -1
    matchs_max = []

    for data in matchs.items():
        season_val, league_val, home_id, away_id, home_goal, away_goal = data

        if season_val != saison or int(league_val) != int(league_id):
            continue

        try:
            diff = abs(int(home_goal) - int(away_goal))
        except (ValueError, TypeError):
            continue

        if diff > max_diff:
            max_diff = diff
            matchs_max = [(home_id, away_id, home_goal, away_goal)]
        elif diff == max_diff:
            matchs_max.append((home_id, away_id, home_goal, away_goal))

    print(
        f"{f'Lors de la saison : {saison}' if saison != '0' else 'Entre 2008'
            ' et 2016'}"
    )
    print(f"{f'en {league}' if league_id != 0 else ''}")
    print(f"l'écart maximal de buts était de {max_diff}\n")

    for home_id, away_id, home_goal, away_goal in matchs_max:
        home_name = teams.get(int(home_id), "Inconnu")
        away_name = teams.get(int(away_id), "Inconnu")
        print(f"{home_name} {home_goal} - {away_goal} {away_name}")
