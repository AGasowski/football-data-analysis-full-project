import pandas as pd
d = pd.read_pickle('Table1.pkl')
#print(d) 
all_teams = d['team_api_id'].unique()
all_saisons = d['saison'].unique()

# Crée toutes les combinaisons possibles (produit cartésien)
import itertools
full_index = pd.DataFrame(list(itertools.product(all_teams, all_saisons)), columns=['team_api_id', 'saison'])
df = pd.merge(full_index, d, on=['team_api_id', 'saison'], how='left')
# Trie par team puis saison (important pour interpolation)
df = df.sort_values(by=['team_api_id', 'saison'])

# Pour pouvoir interpoler, il faut transformer les saisons en nombres
df['saison_num'] = df['saison'].str[:4].astype(int)
 #On remplit chaque colonne (sauf les ID/saison) avec interpolation
colonnes_a_remplir = [col for col in d.columns if col not in ['team_api_id', 'saison']]

for col in colonnes_a_remplir:
    df[col] = df.groupby('team_api_id')[col].transform(lambda x: x.ffill().bfill())
df= df.drop(columns=['saison_num'])  # plus nécessaire
df= df.sort_values(by=['saison', 'team_api_id']).reset_index(drop=True)
df.to_pickle('last_dance.pkl')

