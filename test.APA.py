import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
# IDs de tes deux équipes
team1_id = 8633
team2_id = 8634

# Charger les données
match_df = pd.read_pickle('match.pkl')
stats_df = pd.read_pickle('enfin.pkl')
# Filtrer les matchs entre team1 et team2 (dans les deux sens)
mask = (
    ((match_df['home_team_api_id'] == team1_id) & (match_df['away_team_api_id'] == team2_id)) |
    ((match_df['home_team_api_id'] == team2_id) & (match_df['away_team_api_id'] == team1_id))
)
match_df = match_df[mask]

# Séparer en données d'entraînement (avant 2014/2015) et données de test
match_train = match_df[match_df['saison'] < '2014/2015']
match_test = match_df[match_df['saison'] == '2014/2015']

# Fusionner avec stats home
stats_home = stats_df.rename(columns=lambda c: f"{c}_home" if c not in ['team_api_id', 'saison'] else c)
match_train = match_train.merge(stats_home, left_on=['home_team_api_id', 'saison'],
                                right_on=['team_api_id', 'saison'], how='left')

# Fusionner avec stats away
stats_away = stats_df.rename(columns=lambda c: f"{c}_away" if c not in ['team_api_id', 'saison'] else c)
match_train = match_train.merge(stats_away, left_on=['away_team_api_id', 'saison'],
                                right_on=['team_api_id', 'saison'], how='left')

# Colonnes explicatives


# Liste des colonnes à exclure : 'team_api_id' et 'saison'
exclude_columns = ['team_api_id', 'saison']

# Extraire toutes les colonnes de statistiques sauf celles à exclure
stat_columns = [col for col in stats_df.columns if col not in exclude_columns]

# Créer feature_cols en utilisant les colonnes extraites de stat_equipe
feature_cols = [col for col in match_train.columns if any(stat in col for stat in stat_columns)]


# Variables explicatives (X) et cibles (y)
X_train = match_train[feature_cols].dropna()
y_train = match_train[['home_team_goal', 'away_team_goal']].loc[X_train.index]

# Normaliser les données
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
# Entraîner modèle avec les données normalisées
model = LinearRegression()
model.fit(X_train_scaled, y_train)

print("Poids des caractéristiques :", model.coef_)
print("Intercept :", model.intercept_)
'''
### Prédiction pour 2014/2015
match_test = match_test.merge(stats_home, left_on=['home_team_api_id', 'saison'],
                              right_on=['team_api_id', 'saison'], how='left')
match_test = match_test.merge(stats_away, left_on=['away_team_api_id', 'saison'],
                              right_on=['team_api_id', 'saison'], how='left')

X_test = match_test[feature_cols].dropna()
# Normaliser les données de test
X_test_scaled = scaler.transform(X_test)
# Prédiction
if not X_test.empty:
    y_pred = model.predict(X_test_scaled)
    print("Prédiction du score du match 2014/2015 entre les deux équipes :")
    print(y_pred)
else:
    print("Données insuffisantes pour faire une prédiction.")
'''
