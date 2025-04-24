from fonctions_utiles_panda import (
    lire_csv,
    select_saison,
    convertir_int,
    convertir_list,
    calcul_liste,
    diff_abs,
)

match = lire_csv("data/Match.csv")
match = select_saison(match, "2014/2015")
team = lire_csv("data/Team.csv")

convertir_int(match, "home_team_api_id")
convertir_int(match, "away_team_api_id")
convertir_int(team, "team_api_id")


home_goal = convertir_list(match, "home_team_goal")
away_goal = convertir_list(match, "away_team_goal")
home_team = convertir_list(match, "home_team_api_id")
away_team = convertir_list(match, "away_team_api_id")
team_name = convertir_list(team, "team_long_name")
team_id = convertir_list(team, "team_api_id")

Ecart = calcul_liste([home_goal, away_goal], diff_abs)

match["home_team_api_id"].mean()
ecart_max = max(Ecart)


def liaison_table(A, B, i):
    for j in range(len(A)):
        if A[j] == i:
            return B[j]


for i in range(len(Ecart)):
    if Ecart[i] == ecart_max:
        print(
            liaison_table(team_id, team_name, home_team[i]),
            liaison_table(team_id, team_name, away_team[i]),
            home_goal[i],
            away_goal[i],
        )
