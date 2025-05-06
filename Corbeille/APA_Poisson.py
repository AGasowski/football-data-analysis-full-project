from fonction_commune_chahid import *
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import PoissonRegressor

df_equipe = pd.read_excel("stats_equipes.xlsx")
df_match = pd.read_excel("match.xlsx")

# Jointure pour les équipes à domicile
df_match = df_match.merge(
    df_equipe,
    left_on=["home_team_api_id", "saison"],
    right_on=["team_api_id", "saison"],
    how="left",
    suffixes=("", "_h"),  # Ajoute le suffixe _h pour éviter les conflits
)

# Renommage des colonnes pour l'équipe à domicile
df_match = df_match.rename(
    columns=lambda x: (
        x + "_h" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x
    )
)

# Jointure pour les équipes à l'extérieur
df_match = df_match.merge(
    df_equipe,
    left_on=["away_team_api_id", "saison"],
    right_on=["team_api_id", "saison"],
    how="left",
    suffixes=("", "_a"),
)

# Renommage des colonnes pour l'équipe à l'extérieur
df_match = df_match.rename(
    columns=lambda x: (
        x + "_a" if x in df_equipe.columns and x not in ["team_api_id", "saison"] else x
    )
)

features = [
    "moyenne_attributs_buteur_h",
    "moyenne_attributs_passeur_h",
    "age_moyen_buteur_h",
    "age_moyen_passeur_h",
    "ratio_but_tir_cadre_h",
    "ratio_tir_cadre_tir_non_cadre_h",
    "y_cards_per_match_h",
    "match_count_x_h",
    "r_cards_per_match_h",
    "match_count_y_h",
    "nb_scorers_h",
    "nb_assisters_h",
    "nb_unique_contributors_h",
    "buildUpPlaySpeed_h",
    "buildUpPlayDribbling_h",
    "buildUpPlayPassing_h",
    "chanceCreationPassing_h",
    "chanceCreationCrossing_h",
    "defencePressure_h",
    "defenceAggression_h",
    "defenceTeamWidth_h",
    "moyenne_attributs_buteur_a",
    "moyenne_attributs_passeur_a",
    "age_moyen_buteur_a",
    "age_moyen_passeur_a",
    "ratio_but_tir_cadre_a",
    "ratio_tir_cadre_tir_non_cadre_a",
    "y_cards_per_match_a",
    "match_count_x_a",
    "r_cards_per_match_a",
    "match_count_y_a",
    "nb_scorers_a",
    "nb_assisters_a",
    "nb_unique_contributors_a",
    "buildUpPlaySpeed_a",
    "buildUpPlayDribbling_a",
    "buildUpPlayPassing_a",
    "chanceCreationPassing_a",
    "chanceCreationCrossing_a",
    "defencePressure_a",
    "defenceAggression_a",
    "defenceTeamWidth_a",
]

df_match_clean = df_match.dropna()


# Variables cibles
y_home = df_match_clean["home_team_goal"]
y_away = df_match_clean["away_team_goal"]

X = df_match_clean[features]

# Séparer les données pour entraîner/évaluer
X_train, X_test, y_home_train, y_home_test = train_test_split(
    X, y_home, test_size=0.2, random_state=42
)
_, _, y_away_train, y_away_test = train_test_split(
    X, y_away, test_size=0.2, random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Modèle pour les buts de l'équipe à domicile
model_home = PoissonRegressor(alpha=1e-12, max_iter=300)
model_home.fit(X_train_scaled, y_home_train)

# Modèle pour les buts de l'équipe à l'extérieur
model_away = PoissonRegressor(alpha=1e-12, max_iter=300)
model_away.fit(X_train_scaled, y_away_train)

y_home_pred = model_home.predict(X_test_scaled)
y_away_pred = model_away.predict(X_test_scaled)

# MSE
print("MSE home:", mean_squared_error(y_home_test, y_home_pred))
print("MSE away:", mean_squared_error(y_away_test, y_away_pred))

# R²
print("R² home:", r2_score(y_home_test, y_home_pred))
print("R² away:", r2_score(y_away_test, y_away_pred))


df_sample = df_match_clean[
    (df_match_clean["home_team_api_id"] == 8633)
    & (df_match_clean["away_team_api_id"] == 8634)
]

# Moyenne des features de ces matchs
X_input = df_sample[features]
# Standardisation avec le scaler déjà entraîné
X_input_scaled = scaler.transform(X_input)

# Prédiction
prediction_home = model_home.predict(X_input_scaled)
prediction_away = model_away.predict(X_input_scaled)
home_goals, away_goals = prediction_home[0], prediction_away[0]
print(f"Score prédit : {home_goals:.1f} - {away_goals:.1f}")
