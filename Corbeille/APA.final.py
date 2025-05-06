
import pandas as pd
d1 = pd.read_pickle('last_dance.pkl')
d2 = pd.read_pickle('table_chahid.pkl')

d1['team_api_id'] = d1['team_api_id'].astype(int)
d2['team_api_id'] = d2['team_api_id'].astype(int)

# (si besoin aussi pour la saison)
d1['saison'] = d1['saison'].astype(str)
d2['saison'] = d2['saison'].astype(str)
df_final = pd.merge(d1, d2, on=['team_api_id', 'saison'], how='inner')
df_final.to_pickle('fusion.pkl') 
