
import pandas as pd 
pd.set_option('display.max_columns', 100)


df_stats=pd.read_pickle('match.pkl')
id_team_A = 8633
id_team_B = 8634

# Filtrage de la table des statistiques
df_stats_filtered = df_stats[df_stats['team_api_id'].isin([id_team_A, id_team_B])]
print(df_stats_filtered) 