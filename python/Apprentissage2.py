from fonction_commune_chahid import *
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from change import *

df_equipe = pd.read_excel("stats_equipes.xlsx")
df_titulaire = pd.read_excel("titulaire.xlsx")
df_equipe = fusionner(
    df_equipe, df_titulaire, ["team_api_id", "saison"], ["team_api_id", "season"]
)

df_match = pd.read_excel("match2.xlsx")
print(df_match.columns)
team = lire_csv("data/Team.csv")
"""
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
    "moyenne_overall_titulaire_h",
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
    "moyenne_overall_titulaire_a",
]


# Étape 1 : nettoyage
df_match_clean = df_match.dropna()

# Étape 2 : X et y
X = df_match_clean[features]
y = df_match_clean[["home_team_goal", "away_team_goal"]]

# Étape 3 : train/test split
df_2008 = df_match_clean[df_match_clean["saison"] == "2008/2009"]
# Suppose que df est ton DataFrame
# Assure-toi que la colonne 'date' est bien en datetime


# Trie les matchs par date
df_2008 = df_2008.sort_values("date")

# Concatène tous les matchs joués par chaque équipe (à domicile ou à l'extérieur)
home_matches = df_2008[["date", "home_team_api_id"]].rename(
    columns={"home_team_api_id": "team"}
)
away_matches = df_2008[["date", "away_team_api_id"]].rename(
    columns={"away_team_api_id": "team"}
)

all_matches = pd.concat([home_matches, away_matches])
all_matches = all_matches.sort_values("date")

# Numérote les matchs par équipe
all_matches["match_number"] = all_matches.groupby("team").cumcount() + 1

# Ne garde que les 20 premiers matchs pour chaque équipe
valid_matches = all_matches[all_matches["match_number"] <= 20]

print(valid_matches[valid_matches["league_id"] == 1729])
"""
"""
X_train = train[features]
y_train = train[["home_team_goal", "away_team_goal"]]

X_test = test[features]
y_test = test[["home_team_goal", "away_team_goal"]]
"""
