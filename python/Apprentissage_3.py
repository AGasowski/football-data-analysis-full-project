import pandas as pd

# Paramètres
SAISON_CIBLE = '2012/2013'
LIGUE_CIBLE = 1729  # À adapter
MATCHES_JOUE_19 = 19
df = pd.read_csv("data/Match.csv")

# Filtrer la saison et la ligue
df_season = df[(df['season'] == SAISON_CIBLE) & (df['league_id'] == LIGUE_CIBLE)].copy()

# Trier par date
df_season['date'] = pd.to_datetime(df_season['date'])
df_season = df_season.sort_values('date')

# Créer des colonnes pour le comptage des matchs joués par chaque équipe
df_season['home_matches'] = df_season.groupby('home_team_api_id')['home_team_api_id'].transform('count')
df_season['away_matches'] = df_season.groupby('away_team_api_id')['away_team_api_id'].transform('count')
df_season['total_matches_played'] = df_season['home_matches'] + df_season['away_matches']

# Créer un dictionnaire pour suivre les stats des équipes à chaque moment
team_stats = {}

data = []

# Parcourir tous les matchs de la saison
for _, row in df_season.iterrows():
    home_team = row['home_team_api_id']
    away_team = row['away_team_api_id']
    
    # Mise à jour des statistiques pour les équipes à domicile et à l'extérieur
    for team in [home_team, away_team]:
        if team not in team_stats:
            team_stats[team] = {
                'points': 0,
                'goal_diff': 0,
                'goals_scored': 0,
                'goals_conceded': 0,
                'wins': 0,
                'draws': 0,
                'losses': 0,
                'home_matches': 0,
                'away_matches': 0,
                'results': []
            }
        
        # Calcul des buts marqués et encaissés
        if team == home_team:
            scored = row['home_team_goal']
            conceded = row['away_team_goal']
            team_stats[team]['home_matches'] += 1
        else:
            scored = row['away_team_goal']
            conceded = row['home_team_goal']
            team_stats[team]['away_matches'] += 1
        
        # Mettre à jour les buts marqués et encaissés
        team_stats[team]['goals_scored'] += scored
        team_stats[team]['goals_conceded'] += conceded
        team_stats[team]['goal_diff'] += (scored - conceded)

        # Calcul des résultats
        if scored > conceded:
            team_stats[team]['wins'] += 1
            team_stats[team]['points'] += 3
            team_stats[team]['results'].append(3)
        elif scored == conceded:
            team_stats[team]['draws'] += 1
            team_stats[team]['points'] += 1
            team_stats[team]['results'].append(1)
        else:
            team_stats[team]['losses'] += 1
            team_stats[team]['results'].append(0)
        
        # Une fois que l'équipe a joué 19 matchs, on récupère les stats
        if team_stats[team]['home_matches'] + team_stats[team]['away_matches'] == MATCHES_JOUE_19:
            form_last_5 = sum(team_stats[team]['results'][-5:])
            data.append({
                'team_id': team,
                'points': team_stats[team]['points'],
                'goal_diff': team_stats[team]['goal_diff'],
                'goals_scored': team_stats[team]['goals_scored'],
                'goals_conceded': team_stats[team]['goals_conceded'],
                'wins': team_stats[team]['wins'],
                'draws': team_stats[team]['draws'],
                'losses': team_stats[team]['losses'],
                'form_last_5': form_last_5,
                'home_matches': team_stats[team]['home_matches'],
                'away_matches': team_stats[team]['away_matches']
            })
            # Retirer les statistiques de l'équipe après avoir pris ses données
            del team_stats[team]

# Créer un DataFrame à partir des données collectées
df_features = pd.DataFrame(data)

# Calculer le classement à ce moment-là
df_features = df_features.sort_values(by=['points', 'goal_diff', 'goals_scored'], ascending=False)
df_features['rank_at_19_matches'] = range(1, len(df_features) + 1)

# Affichage du résultat
print(df_features.head())
