import numpy as np
import pandas as pd
from sklearn.linear_model import PoissonRegressor
from sklearn.preprocessing import StandardScaler
from change import *
from fonction_commune_chahid import *

# Chargement des données
df_equipe = pd.read_excel("stats_equipes.xlsx")
df_titulaire = pd.read_excel("titulaire.xlsx")
df_match = pd.read_excel("match.xlsx")
team = lire_csv("data/Team.csv")

# Fusion
df_equipe = fusionner(df_equipe, df_titulaire, ["team_api_id", "saison"], ["team_api_id", "season"])

# Jointures
df_match = df_match.merge(df_equipe, left_on=["home_team_api_id", "saison"], right_on=["team_api_id", "saison"], how="left", suffixes=("", "_h"))
df_match = df_match.rename(columns=lambda x: x + "_h" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x)

df_match = df_match.merge(df_equipe, left_on=["away_team_api_id", "saison"], right_on=["team_api_id", "saison"], how="left", suffixes=("", "_a"))
df_match = df_match.rename(columns=lambda x: x + "_a" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x)

# Sélection des features
features = [
    "moyenne_overall_titulaire_h", "moyenne_attributs_buteur_h", "moyenne_attributs_passeur_h", "age_moyen_buteur_h",
    "age_moyen_passeur_h", "ratio_but_tir_cadre_h", "ratio_tir_cadre_tir_non_cadre_h", "y_cards_per_match_h",
    "r_cards_per_match_h", "nb_unique_contributors_h", "buildUpPlaySpeed_h", "buildUpPlayDribbling_h",
    "buildUpPlayPassing_h", "chanceCreationPassing_h", "chanceCreationCrossing_h", "defencePressure_h",
    "defenceAggression_h", "defenceTeamWidth_h", "moyenne_attributs_buteur_a", "moyenne_attributs_passeur_a",
    "age_moyen_buteur_a", "age_moyen_passeur_a", "ratio_but_tir_cadre_a", "ratio_tir_cadre_tir_non_cadre_a",
    "y_cards_per_match_a", "r_cards_per_match_a", "nb_unique_contributors_a", "buildUpPlaySpeed_a",
    "buildUpPlayDribbling_a", "buildUpPlayPassing_a", "chanceCreationPassing_a", "chanceCreationCrossing_a",
    "defencePressure_a", "defenceAggression_a", "defenceTeamWidth_a", "moyenne_overall_titulaire_a"
]

# Nettoyage
df_match_clean = df_match.dropna()
train = df_match_clean[df_match_clean["saison"] < "2014/2015"]
test = df_match_clean[df_match_clean["saison"] == "2014/2015"]

X_train = train[features]
y_train_home = train["home_team_goal"]
y_train_away = train["away_team_goal"]
X_test = test[features]

# Standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modèle Poisson pour prédictions des buts
poisson_home = PoissonRegressor()
poisson_away = PoissonRegressor()

# Entraînement du modèle pour les buts à domicile
poisson_home.fit(X_train_scaled, y_train_home)

# Entraînement du modèle pour les buts à l'extérieur
poisson_away.fit(X_train_scaled, y_train_away)

# Prédictions
pred_home = poisson_home.predict(X_test_scaled)
pred_away = poisson_away.predict(X_test_scaled)

# Classement
df_2014 = test.copy()
classement = []

for i, row in enumerate(df_2014.itertuples()):
    id1 = row.home_team_api_id
    id2 = row.away_team_api_id
    league_id = row.league_id

    home_goals = round(pred_home[i])
    away_goals = round(pred_away[i])

    if home_goals > away_goals:
        points_home, points_away = 3, 0
    elif home_goals < away_goals:
        points_home, points_away = 0, 3
    else:
        points_home = points_away = 1

    classement.append({
        "team_api_id": id1,
        "league_id": league_id,
        "points": points_home,
        "but_marques": home_goals,
        "but_encaisses": away_goals,
    })
    classement.append({
        "team_api_id": id2,
        "league_id": league_id,
        "points": points_away,
        "but_marques": away_goals,
        "but_encaisses": home_goals,
    })

df_classement = pd.DataFrame(classement)
df_resultats = df_classement.groupby(["league_id", "team_api_id"]).agg(
    points_total=("points", "sum"),
    buts_marques=("but_marques", "sum"),
    buts_encaisses=("but_encaisses", "sum"),
).reset_index()

df_resultats = df_resultats.sort_values(["league_id", "points_total"], ascending=[True, False])
df_resultats["team_api_id"] = df_resultats["team_api_id"].apply(id_to_nom)

print(df_resultats[df_resultats["league_id"] == 4769])
