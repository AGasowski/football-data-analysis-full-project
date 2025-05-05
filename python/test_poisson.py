from fonction_commune_chahid import *
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import PoissonRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from change import *
import numpy as np
import pandas as pd

# Chargement des données
df_equipe = pd.read_excel("stats_equipes.xlsx")
df_titulaire = pd.read_excel("titulaire.xlsx")
df_equipe = fusionner(df_equipe, df_titulaire, ["team_api_id", "saison"], ["team_api_id", "season"])
df_match = pd.read_excel("match.xlsx")
team = lire_csv("data/Team.csv")

# Jointures
df_match = df_match.merge(df_equipe, left_on=["home_team_api_id", "saison"], right_on=["team_api_id", "saison"], how="left", suffixes=("", "_h"))
df_match = df_match.rename(columns=lambda x: x + "_h" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x)

df_match = df_match.merge(df_equipe, left_on=["away_team_api_id", "saison"], right_on=["team_api_id", "saison"], how="left", suffixes=("", "_a"))
df_match = df_match.rename(columns=lambda x: x + "_a" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x)

# Features
features = [
    "moyenne_overall_titulaire_h", "moyenne_attributs_buteur_h", "moyenne_attributs_passeur_h",
    "age_moyen_buteur_h", "age_moyen_passeur_h", "ratio_but_tir_cadre_h", "ratio_tir_cadre_tir_non_cadre_h",
    "y_cards_per_match_h", "r_cards_per_match_h", "nb_unique_contributors_h", "buildUpPlaySpeed_h",
    "buildUpPlayDribbling_h", "buildUpPlayPassing_h", "chanceCreationPassing_h", "chanceCreationCrossing_h",
    "defencePressure_h", "defenceAggression_h", "defenceTeamWidth_h",
    "moyenne_attributs_buteur_a", "moyenne_attributs_passeur_a", "age_moyen_buteur_a", "age_moyen_passeur_a",
    "ratio_but_tir_cadre_a", "ratio_tir_cadre_tir_non_cadre_a", "y_cards_per_match_a", "r_cards_per_match_a",
    "nb_unique_contributors_a", "buildUpPlaySpeed_a", "buildUpPlayDribbling_a", "buildUpPlayPassing_a",
    "chanceCreationPassing_a", "chanceCreationCrossing_a", "defencePressure_a", "defenceAggression_a",
    "defenceTeamWidth_a", "moyenne_overall_titulaire_a"
]

# Nettoyage
df_match_clean = df_match.dropna()
X = df_match_clean[features]
y_home = df_match_clean["home_team_goal"]
y_away = df_match_clean["away_team_goal"]

# Split
train = df_match_clean[df_match_clean["saison"] < "2014/2015"]
test = df_match_clean[df_match_clean["saison"] == "2014/2015"]

X_train = train[features]
y_train_home = train["home_team_goal"]
y_train_away = train["away_team_goal"]

X_test = test[features]
y_test_home = test["home_team_goal"]
y_test_away = test["away_team_goal"]

# Standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
moyennes = pd.Series(scaler.mean_, index=X_train.columns, name="Moyenne")
ecarts_type = pd.Series(scaler.scale_, index=X_train.columns, name="Écart-type")

# Régressions de Poisson
model_home = PoissonRegressor(alpha=1e-12, max_iter=300)
model_away = PoissonRegressor(alpha=1e-12, max_iter=300)
model_home.fit(X_train_scaled, y_train_home)
model_away.fit(X_train_scaled, y_train_away)

def fonction(id1, id2, df_base):
    d = df_base[(df_base["home_team_api_id"] == id1) & (df_base["away_team_api_id"] == id2)]
    return d[features]

# Prédictions et classement
df_2014 = df_match_clean[df_match_clean["saison"] == "2014/2015"].copy()
classement = []

for _, row in df_2014.iterrows():
    id1 = row["home_team_api_id"]
    id2 = row["away_team_api_id"]
    league_id = row["league_id"]

    X_input = fonction(id1, id2, df_2014)
    if X_input.empty:
        continue

    X_scaled = (X_input - moyennes) / ecarts_type

    mu_home = model_home.predict(X_scaled)[0]
    mu_away = model_away.predict(X_scaled)[0]

    # Tirage aléatoire à partir de la loi de Poisson
    #np.random.seed(42)  # Fixe la graine pour des résultats reproductibles
# Intervalle de confiance pour les prédictions de Poisson
    confidence_interval_home = (mu_home - 1.96 * np.sqrt(mu_home), mu_home + 1.96 * np.sqrt(mu_home))
    confidence_interval_away = (mu_away - 1.96 * np.sqrt(mu_away), mu_away + 1.96 * np.sqrt(mu_away))

# Tirage des buts avec l'intervalle de confiance
    home_goals_lower = np.random.poisson(confidence_interval_home[0])
    home_goals_upper = np.random.poisson(confidence_interval_home[1])
    away_goals_lower = np.random.poisson(confidence_interval_away[0])
    away_goals_upper = np.random.poisson(confidence_interval_away[1])

# Tu peux décider de choisir un des tirages ou bien de prendre la moyenne des résultats
    home_goals = (home_goals_lower + home_goals_upper) / 2
    away_goals = (away_goals_lower + away_goals_upper) / 2   

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
