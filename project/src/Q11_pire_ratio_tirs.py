from project.src.fonctions.data_loader import charger_csv, data_to_dict
from project.src.fonctions.manipulations import (
    filtrer_df,
    name_team_dic,
    cle_extreme,
)
from project.src.fonctions.statistiques import (
    calculer_moyenne,
)


def run_q11(saison):
    print("== Résolution de la question 11 ==")

    match = charger_csv("data/Match.csv")
    if saison != 0:
        match = filtrer_df(match, "season", saison)
    match = filtrer_df(match, "league_id", 21518)
    match = filtrer_df(
        match,
        None,
        None,
        ["home_team_api_id", "home_team_goal", "away_team_goal", "shoton"],
    )
    team = charger_csv("data/Team.csv")
    team = filtrer_df(team, None, None, ["team_api_id", "team_long_name"])

    match["but"] = match["home_team_goal"] + match["away_team_goal"]
    match["tir_cadre"] = match["shoton"].map(
        lambda x: (len(x) if isinstance(x, (list, str)) and x != "" else 1)
    )
    match["ratio"] = match["but"] / match["tir_cadre"]
    d = calculer_moyenne(match, "home_team_api_id", "ratio")
    team_names = data_to_dict(team, "team_api_id", "team_long_name")
    print(name_team_dic(team_names, cle_extreme(d, "min")))
