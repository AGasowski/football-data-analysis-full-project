
import pandas as pd
team = pd.read_csv("data/Team_Attributes.csv")
team['date'] = pd.to_datetime(team['date'])

# Fonction pour transformer une date en saison
def date_en_saison(date):
    if date.month >= 8:
        return f"{date.year}/{date.year + 1}"
    else:
        return f"{date.year - 1}/{date.year}"

# Appliquer la fonction
team['saison'] = team['date'].apply(date_en_saison) 
team = team[~team['saison'].isin(['2016/2017', '2006/2007', '2007/2008'])]
team = team[['team_api_id', 'saison', 'buildUpPlaySpeed','buildUpPlayDribbling','buildUpPlayPassing','chanceCreationPassing','chanceCreationCrossing','defencePressure','defenceAggression','defenceTeamWidth']]

colonnes_a_ignorer = ['team_api_id', 'saison']

# Colonnes concernées par le remplacement
colonnes_a_verifier = [col for col in team.columns if col not in colonnes_a_ignorer]

# Appliquer le remplacement ligne par ligne
def remplir_nan_ligne(row):
    max_val = row[colonnes_a_verifier].max(skipna=True)
    return row[colonnes_a_verifier].fillna(max_val)

# Appliquer le remplissage ligne par ligne, sans toucher aux colonnes ignorées
team[colonnes_a_verifier] = team.apply(lambda row: remplir_nan_ligne(row), axis=1)


# Étape 1 — Liste complète des saisons à couvrir
saisons_completes = [f"{y}/{y+1}" for y in range(2008, 2016 + 1)]

# Étape 2 — Toutes les équipes existantes
teams_uniques = team['team_api_id'].unique()

# Étape 3 — Création de toutes les combinaisons possibles
base_complete = pd.MultiIndex.from_product(
    [teams_uniques, saisons_completes],
    names=['team_api_id', 'saison']
).to_frame(index=False)

# Étape 4 — Fusion avec ta table
df_complete = pd.merge(base_complete, team, on=['team_api_id', 'saison'], how='left')

# Étape 5 — Remplir les lignes manquantes avec la saison la plus proche
def remplir_ligne_manquante(row, data_grouped):
    if pd.isna(row).any():
        equipe = row['team_api_id']
        saison = row['saison']
        
        # Extraire les lignes non nulles pour cette équipe
        lignes_connues = data_grouped.get(equipe, [])
        if not lignes_connues.empty:
            return row  # Aucun backup possible
        
        # Trouver la saison la plus proche
        saison_num = int(saison[:4])
        lignes_connues['distance'] = lignes_connues['saison'].str[:4].astype(int).sub(saison_num).abs()
        plus_proche = lignes_connues.sort_values('distance').iloc[0]
        
        # Remplir la ligne
        for col in df.columns:
            if pd.isna(row[col]) and col not in ['team_api_id', 'saison']:
                row[col] = plus_proche[col]
    return row

# Regrouper les lignes valides par équipe
df_valides = team.dropna()
grouped_dict = {
    team_id: group.copy()
    for team_id, group in df_valides.groupby('team_api_id')
}

# Appliquer la logique à chaque ligne
df_complete = df_complete.apply(lambda row: remplir_ligne_manquante(row, grouped_dict), axis=1)
def remplacer_nan_par_proche(df):
    # Pour chaque équipe et chaque saison, on remplace les NaN par la saison la plus proche
    for team_id in df['team_api_id'].unique():
        team_data = df[df['team_api_id'] == team_id]
        
        # Pour chaque ligne de cette équipe
        for index, row in team_data.iterrows():
            # Si la ligne contient des NaN
            if row.isna().any():
                # Filtrer les saisons valides (sans NaN)
                saisons_valides = team_data.dropna(subset=[col for col in df.columns if col not in ['team_api_id', 'saison']])

                # Si il n'y a pas de lignes valides pour cette équipe, continuer
                if saisons_valides.empty:
                    continue

                # Trouver la saison la plus proche, qu'elle soit dans le passé ou le futur
                saison_num = int(row['saison'][:4])
                saisons_valides['distance'] = saisons_valides['saison'].str[:4].astype(int).sub(saison_num).abs()
                
                # Trouver la saison la plus proche, qu'elle soit dans le passé ou le futur
                plus_proche = saisons_valides.sort_values('distance').iloc[0]
                
                # Remplacer les NaN de la ligne par la saison la plus proche
                for col in df.columns:
                    if pd.isna(row[col]) and col not in ['team_api_id', 'saison']:
                        df.at[index, col] = plus_proche[col]
    
    return df
df_complete = remplacer_nan_par_proche(df_complete)
fusion=pd.read_pickle('fusion.pkl')
df_final = pd.merge(fusion, df_complete, on=['team_api_id', 'saison'], how='inner')
#df_final.to_pickle('enfin.pkl') 
print(df_final)