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
]
df_match_clean = df_match.dropna()

X = df_match_clean[features]
y = df_match_clean[["home_team_goal", "away_team_goal"]]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# Puis tu continues normalement :
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

model = LinearRegression()
model.fit(X_train, y_train)
# print("Coefficients :", model.coef_)
# print("Intercept :", model.intercept_)
y_pred = model.predict(X_test)
# print(y_pred)
# print("MSE :", mean_squared_error(y_test, y_pred))
# print("R² :", r2_score(y_test, y_pred))


df_historique = df_match_clean[
    (
        (df_match_clean["home_team_api_id"] == 8633)
        & (df_match_clean["away_team_api_id"] == 8634)
    )
    | (
        (df_match_clean["home_team_api_id"] == 8634)
        & (df_match_clean["away_team_api_id"] == 8633)
    )
]

df_sample = df_match_clean[
    (df_match_clean["home_team_api_id"] == 8633)
    & (df_match_clean["away_team_api_id"] == 8634)
]

X_input = df_sample[features].mean().to_frame().T  # 1 ligne moyenne

prediction = model.predict(X_input)
home_goals, away_goals = prediction[0]
print(f"Score prédit : {home_goals:.1f} - {away_goals:.1f}")
