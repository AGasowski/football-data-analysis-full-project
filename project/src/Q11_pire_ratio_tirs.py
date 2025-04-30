from project.src.fonctions_communes import (
    lire_csv,
    select_all,
    select_colonnes,
    name_team_dic,
    data_to_dict,
    moyenne_par_colonne,
    cle_minimale,
)


def run_q11():
    print("== Résolution de la question 11 ==")

    match = lire_csv("data/Match.csv")
    match = select_all(match, "season", "2014/2015")
    match = select_all(match, "league_id", 21518)
    match = select_colonnes(
        match,
        ["home_team_api_id", "home_team_goal", "away_team_goal", "shoton"],
    )
    team = lire_csv("data/Team.csv")
    team = select_colonnes(team, ["team_api_id", "team_long_name"])

    match["but"] = match["home_team_goal"] + match["away_team_goal"]
    match["tir_cadre"] = match["shoton"].map(
        lambda x: len(x) if x not in [""] and len(x) > 0 else 1
    )
    match["ratio"] = match["but"] / match["tir_cadre"]
    d = moyenne_par_colonne(match, "home_team_api_id", "ratio")
    team_names = data_to_dict(team, "team_api_id", "team_long_name")
    print(name_team_dic(team_names, cle_minimale(d)))
