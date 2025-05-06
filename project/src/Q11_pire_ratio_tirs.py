"""
Script pour dentifier l'équipe avec le pire ratio entre les buts marqués et
les tirs cadrés dans une saison donnée.
"""

from project.src.fonctions.data_loader import charger_csv, data_to_dict
from project.src.fonctions.manipulations import (
    filtrer_df,
    name_team_dic,
    cle_extreme,
    id_championnat,
)
from project.src.fonctions.statistiques import (
    calculer_moyenne,
)


def run_q11(saison, championnat):
    """
    Affiche l’équipe avec le pire ratio entre buts marqués et tirs cadrés.

    Args:
        saison (str): Saison ciblée, par exemple "2014/2015". championnat
        (str): Nom du championnat
    """
    print("Equipe avec le pire ratio buts marqués/tirs cadrés")
    print(f"en {championnat} ({saison}):")

    match = charger_csv("data/Match.csv")
    if saison != "0":
        match = filtrer_df(match, "season", saison)
    id_champ = id_championnat(championnat)
    if id_champ != 0:
        match = filtrer_df(match, "league_id", int(id_champ))
    match = filtrer_df(
        match,
        None,
        None,
        ["home_team_api_id", "home_team_goal", "away_team_goal", "shoton"],
    )
    print(match)
    team = charger_csv("data/Team.csv")
    team = filtrer_df(team, None, None, ["team_api_id", "team_long_name"])

    match["but"] = match["home_team_goal"] + match["away_team_goal"]
    match["tir_cadre"] = match["shoton"].map(
        lambda x: (len(x) if isinstance(x, (list, str)) and x != "" else 1)
    )
    match["ratio"] = match["but"] / (match["but"] + match["tir_cadre"])
    d = calculer_moyenne(match, "home_team_api_id", "ratio")
    team_names = data_to_dict(team, "team_api_id", "team_long_name")
    print(name_team_dic(team_names, cle_extreme(d, "min")))


run_q11("2012/2014", "Premier League (Angleterre)")
