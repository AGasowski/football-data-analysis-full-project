import pandas as pd

fichier_source = "data/Match.csv"
df = pd.read_csv(fichier_source)
df_selectionne = df[["id", "country_id", "league_id", "season", "match_api_id", "home_team_api_id", "away_team_api_id", "home_team_goal", "away_team_goal"]]

data_team = "data/Team.csv"
team = pd.read_csv(data_team)
df1 = df[["home_team_api_id"]]
df2 = team[["team_api_id", "team_long_name"]]
team_name_home = pd.merge(df1, df2, left_on='home_team_api_id', right_on='team_api_id', how='inner')
team_name_home = team_name_home.drop_duplicates()
team_name_home = team_name_home.rename(columns={"team_long_name": "team_home_name"})


df3 = df[["away_team_api_id"]]
team_name_away = pd.merge(df3, df2, left_on='away_team_api_id', right_on='team_api_id', how='inner')
team_name_away = team_name_away.drop_duplicates()
team_name_away = team_name_away.rename(columns={"team_long_name": "team_away_name"})


df_final = pd.merge(team_name_home, df_selectionne, left_on='home_team_api_id', right_on='home_team_api_id',how='inner')
df_final = pd.merge(df_final, team_name_away,  left_on='away_team_api_id', right_on='away_team_api_id', how='inner')

# print(f"Le fichier {df_selectionne} a été créé avec succès !")
df_Saison_1 = df_final[df_final["season"] == "2012/2013"]

leagues = df_Saison_1["league_id"].unique()

classements = []

for league_id in leagues:
    print(f"Traitement de la league {league_id}...")

    # Filtrer les matchs de la saison en cours
    df_Saison_1_league = df_Saison_1[df_Saison_1["league_id"] == league_id]

    # Initialiser un dictionnaire pour stocker les stats des équipes
    stats = {}

    # Fonction pour mettre à jour les statistiques d'une équipe
    def mettre_a_jour_stats(equipe, points_gagnes, buts_marques, buts_encaisse):
        if equipe not in stats:
            stats[equipe] = {"points": 0, "buts_pour": 0, "buts_contre": 0}

        stats[equipe]["points"] += points_gagnes
        stats[equipe]["buts_pour"] += buts_marques
        stats[equipe]["buts_contre"] += buts_encaisse

    for index, row in df_Saison_1_league.iterrows():
        # Extraire les données du match
        home_team = row["team_home_name"]
        away_team = row["team_away_name"]
        home_goals = row["home_team_goal"]
        away_goals = row["away_team_goal"]
        # Déterminer les points en fonction du score
        if home_goals > away_goals:
            # Victoire à domicile
            mettre_a_jour_stats(home_team, 3, home_goals, away_goals)
            mettre_a_jour_stats(away_team, 0, away_goals, home_goals)
        elif home_goals < away_goals:
            # Victoire à l'extérieur
            mettre_a_jour_stats(home_team, 0, home_goals, away_goals)
            mettre_a_jour_stats(away_team, 3, away_goals, home_goals)
        else:
            # Match nul
            mettre_a_jour_stats(home_team, 1, home_goals, away_goals)
            mettre_a_jour_stats(away_team, 1, away_goals, home_goals)

    # Convertir le dictionnaire en DataFrame
    df_classement = pd.DataFrame.from_dict(stats, orient="index")

    # Ajouter la différence de buts
    df_classement["différence_de_buts"] = df_classement["buts_pour"] - df_classement["buts_contre"]

    # Trier les équipes par points et différence de buts
    df_classement = df_classement.sort_values(by=["points", "différence_de_buts"], ascending=[False, False])

    # Ajouter le classement au dictionnaire général
    classements.append(df_classement)

print("Classement pour toutes les saisons généré avec succès !")

print(classements[5])
