from fonction_commune_chahid import *
from APA_diversite import *
from Corbeille.APA_Carton_rouge import *

diversite_df = diversite_toute_saison()
d = fusionner(
    carton_df, diversite_df, ["team_api_id", "season"], ["team_api_id", "season"]
)
all_teams = d['team_api_id'].unique()
all_saisons = d['season'].unique()

# Crée toutes les combinaisons possibles (produit cartésien)
import itertools
full_index = pd.DataFrame(list(itertools.product(all_teams, all_saisons)), columns=['team_api_id', 'season'])
df = pd.merge(full_index, d, on=['team_api_id', 'season'], how='left')
# Trie par team puis saison (important pour interpolation)
df = df.sort_values(by=['team_api_id', 'season'])

# Pour pouvoir interpoler, il faut transformer les saisons en nombres
df['saison_num'] = df['season'].str[:4].astype(int)
 #On remplit chaque colonne (sauf les ID/saison) avec interpolation
colonnes_a_remplir = [col for col in d.columns if col not in ['team_api_id', 'season']]

for col in colonnes_a_remplir:
    df[col] = df.groupby('team_api_id')[col].transform(lambda x: x.ffill().bfill())
df= df.drop(columns=['saison_num'])  # plus nécessaire
df= df.sort_values(by=['season', 'team_api_id']).reset_index(drop=True)
df.rename(columns={'season': 'saison'}, inplace=True)
df.to_csv('df')
