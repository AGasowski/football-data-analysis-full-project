from fonction_commune_chahid import *
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

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
    "r_cards_per_match_h",
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
    "r_cards_per_match_a",
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


# Étape 1 : nettoyage
df_match_clean = df_match.dropna()

# Étape 2 : X et y
X = df_match_clean[features]
y = df_match_clean[["home_team_goal", "away_team_goal"]]

# Étape 3 : train/test split
train = df_match_clean[df_match_clean["saison"] < "2014/2015"]
test = df_match_clean[df_match_clean["saison"] == "2014/2015"]

X_train = train[features]
y_train = train[["home_team_goal", "away_team_goal"]]

X_test = test[features]
y_test = test[["home_team_goal", "away_team_goal"]]

# Étape 4 : standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Étape 5 : entraînement
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Étape 6 : prédiction sur test set
y_pred = model.predict(X_test_scaled)
print(len(y_pred))
# Étape 7 : évaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("MSE :", mse)
print("R² :", r2)


# Exemple : moyenne des confrontations où 8633 est à domicile et 8634 à l’extérieur
df_sample = df_match_clean[
    (df_match_clean["home_team_api_id"] == 8633)
    & (df_match_clean["away_team_api_id"] == 8634)
]

# Moyenne des features de ces matchs
X_input = df_sample[features]
# Standardisation avec le scaler déjà entraîné
X_input_scaled = scaler.transform(X_input)

# Prédiction
prediction = model.predict(X_input_scaled)
print(prediction)
home_goals, away_goals = prediction[0]
print(f"Score prédit : {home_goals:.1f} - {away_goals:.1f}")
