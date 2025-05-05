import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Charger les données
match = pd.read_csv("data/Match.csv")

match = match[match["league_id"] == 21518]

def fonction(season):
    df_2013 = match[match["season"] == season]
    # Colonnes à garder
    colonnes_a_garder = [
        "home_team_api_id",
        "away_team_api_id",
        "date",
        "home_team_goal",
        "away_team_goal"
    ]

    df_2013_filtré = df_2013[colonnes_a_garder].copy()

    # Fonction pour récupérer les 19 premiers matchs de l'équipe
    def get_first_19_matches(id_equipe):
        # Filtrer les matchs où l'équipe a joué à domicile ou à l'extérieur
        matchs_equipe = df_2013_filtré[
            (df_2013_filtré["home_team_api_id"] == id_equipe) |
            (df_2013_filtré["away_team_api_id"] == id_equipe)
        ].copy()

        # Trier les matchs par date
        matchs_equipe["date"] = pd.to_datetime(matchs_equipe["date"])  # Assure le format datetime
        matchs_equipe = matchs_equipe.sort_values(by="date")

        # Retourner les 19 premiers matchs
        return matchs_equipe.head(19)

    # Fonction pour calculer les statistiques des 19 premiers matchs
    def calculer_stats_19_premiers_matchs(df_ligue_saison, id_equipe):
        # Filtrage des 19 premiers matchs de l'équipe
        premiers_19 = get_first_19_matches(id_equipe)

        # Calcul des points, buts, victoires, etc.
        points = premiers_19["home_team_goal"].where(premiers_19["home_team_api_id"] == id_equipe).sum() + \
                premiers_19["away_team_goal"].where(premiers_19["away_team_api_id"] == id_equipe).sum()

        goal_diff = premiers_19["home_team_goal"].where(premiers_19["home_team_api_id"] == id_equipe).sum() - \
                    premiers_19["away_team_goal"].where(premiers_19["away_team_api_id"] == id_equipe).sum()

        buts_marques = premiers_19["home_team_goal"].where(premiers_19["home_team_api_id"] == id_equipe).sum() + \
                    premiers_19["away_team_goal"].where(premiers_19["away_team_api_id"] == id_equipe).sum()

        buts_encaisses = premiers_19["away_team_goal"].where(premiers_19["home_team_api_id"] == id_equipe).sum() + \
                         premiers_19["home_team_goal"].where(premiers_19["away_team_api_id"] == id_equipe).sum()

        victoires = premiers_19["home_team_goal"].where(premiers_19["home_team_api_id"] == id_equipe).gt(premiers_19["away_team_goal"]).sum() + \
                    premiers_19["away_team_goal"].where(premiers_19["away_team_api_id"] == id_equipe).gt(premiers_19["home_team_goal"]).sum()

        nuls = premiers_19["home_team_goal"].where(premiers_19["home_team_api_id"] == id_equipe).eq(premiers_19["away_team_goal"]).sum() + \
            premiers_19["away_team_goal"].where(premiers_19["away_team_api_id"] == id_equipe).eq(premiers_19["home_team_goal"]).sum()

        defaites = len(premiers_19) - victoires - nuls

        # Calculer les points obtenus lors des 5 derniers matchs
        derniers_5_matchs = premiers_19.tail(5)
        points_5_derniers = 0
        for _, row in derniers_5_matchs.iterrows():
            if row["home_team_api_id"] == id_equipe:
                if row["home_team_goal"] > row["away_team_goal"]:
                    points_5_derniers += 3
                elif row["home_team_goal"] == row["away_team_goal"]:
                    points_5_derniers += 1
            elif row["away_team_api_id"] == id_equipe:
                if row["away_team_goal"] > row["home_team_goal"]:
                    points_5_derniers += 3
                elif row["away_team_goal"] == row["home_team_goal"]:
                    points_5_derniers += 1

        # Récupérer les adversaires des matchs restants (après les 19 premiers matchs)
        adversaires_restants = premiers_19[premiers_19["home_team_api_id"] != id_equipe].copy()
        adversaires_restants = adversaires_restants[adversaires_restants["away_team_api_id"] != id_equipe]

        # Calculer la moyenne des rangs des adversaires restants
        adversaires_restants_avg_rank = adversaires_restants["away_team_api_id"].map(rangs_adversaires).mean()  # rangs_adversaires doit être défini préalablement

        return {
            "equipe": id_equipe,
            "points": points,
            "goal_diff": goal_diff,
            "buts_marques": buts_marques,
            "buts_encaisses": buts_encaisses,
            "victoires": victoires,
            "nuls": nuls,
            "defaites": defaites,
            "forme_5_derniers": points_5_derniers,  # Nombre de points lors des 5 derniers matchs
            "matchs_dom": len(premiers_19[premiers_19["home_team_api_id"] == id_equipe]),
            "matchs_ext": len(premiers_19[premiers_19["away_team_api_id"] == id_equipe]),
            "adversaires_restants_avg_rank": adversaires_restants_avg_rank
        }

    # Liste des équipes présentes
    equipes_saison = pd.unique(df_2013_filtré[["home_team_api_id", "away_team_api_id"]].values.ravel())

    # Dictionnaire pour les rangs des équipes (à remplir)
    rangs_adversaires = {
        # Exemple de données : id_equipe -> rang
        # 1: 5,
        # 2: 8,
        # 3: 3,
        # ...
    }

    # Création du DataFrame final
    stats_equipes = [calculer_stats_19_premiers_matchs(df_2013, id_equipe) for id_equipe in equipes_saison]

    df_stats = pd.DataFrame(stats_equipes)

    # Trier par points et goal_diff
    df_stats = df_stats.sort_values(by=["points", "goal_diff"], ascending=False).reset_index(drop=True)

    # Ajouter la colonne 'rank' (position actuelle de l'équipe)
    df_stats["rank"] = df_stats.index + 1

    # Dictionnaire équipe -> rank actuel
    dict_rank = dict(zip(df_stats["equipe"], df_stats["rank"]))

    # Fonction pour calculer la moyenne des rangs des adversaires restants
    def calcul_avg_rank_restants(id_equipe):
        tous_les_matchs = df_2013_filtré[
            (df_2013_filtré["home_team_api_id"] == id_equipe) |
            (df_2013_filtré["away_team_api_id"] == id_equipe)
        ].copy()
        tous_les_matchs["date"] = pd.to_datetime(tous_les_matchs["date"])
        tous_les_matchs = tous_les_matchs.sort_values(by="date")

        # Matchs restants = total - les 19 premiers
        matchs_restants = tous_les_matchs.iloc[19:]

        adversaires_restants = []
        for _, row in matchs_restants.iterrows():
            if row["home_team_api_id"] == id_equipe:
                adversaire = row["away_team_api_id"]
            else:
                adversaire = row["home_team_api_id"]
            adversaires_restants.append(adversaire)

        # Moyenne des rangs des adversaires
        ranks = [dict_rank.get(ad, None) for ad in adversaires_restants if ad in dict_rank]
        return sum(ranks) / len(ranks) if ranks else None

    # Appliquer la fonction pour calculer les rangs des adversaires restants pour chaque équipe
    df_stats["adversaires_restants_avg_rank"] = df_stats["equipe"].apply(calcul_avg_rank_restants)

    # Colonnes finales à garder
    colonnes_finales = [
        "equipe", "points", "goal_diff", "buts_marques", "buts_encaisses",
        "victoires", "nuls", "defaites", "forme_5_derniers",
        "matchs_dom", "matchs_ext", "rank", "adversaires_restants_avg_rank"
    ]

    # Création du DataFrame final
    df_final = df_stats[colonnes_finales].copy()

    # Affichage du DataFrame final
    #print(df_final)
    def calculer_rang_final(df_saison):
        equipes = pd.unique(df_saison[["home_team_api_id", "away_team_api_id"]].values.ravel())
        stats_finales = []

        for id_equipe in equipes:
            points = 0
            for _, row in df_saison.iterrows():
                if row["home_team_api_id"] == id_equipe:
                    if row["home_team_goal"] > row["away_team_goal"]:
                        points += 3
                    elif row["home_team_goal"] == row["away_team_goal"]:
                        points += 1
                elif row["away_team_api_id"] == id_equipe:
                    if row["away_team_goal"] > row["home_team_goal"]:
                        points += 3
                    elif row["away_team_goal"] == row["home_team_goal"]:
                        points += 1
            stats_finales.append((id_equipe, points))

        df_rang_final = pd.DataFrame(stats_finales, columns=["equipe", "points_fin_saison"])
        df_rang_final = df_rang_final.sort_values(by="points_fin_saison", ascending=False).reset_index(drop=True)
        df_rang_final["rank_final"] = df_rang_final.index + 1
        return df_rang_final

    df_rang_final = calculer_rang_final(df_2013)
    df_final = df_final.merge(df_rang_final[["equipe", "rank_final"]], on="equipe")
    print(df_final)
    return df_final 

# Liste des saisons à traiter
seasons = ["2008/2009", "2009/2010", "2010/2011", "2011/2012", "2012/2013", "2013/2014"]

# Liste pour stocker les DataFrames de chaque saison
df_list = []

# Boucle sur chaque saison
for season in seasons:
    df_season = fonction(season)  # Appeler la fonction pour chaque saison
    df_list.append(df_season)  # Ajouter le DataFrame

# Concatenation de tous les DataFrames en un seul
df_final = pd.concat(df_list, ignore_index=True)

# 1. Utiliser df_final pour l'entraînement (tu l'as déjà créé, c'est bien ton jeu d'entraînement)
df_train = df_final

# 2. Pour le test, supposons que tu as les données de la saison 2014/2015
# Tu peux les charger dans un DataFrame séparé (par exemple df_test pour la saison 2014/2015)
# Je suppose ici que df_test contient les stats pour la saison 2014/2015
df_test = fonction("2014/2015")  # Remplace df_saison_test par le vrai DataFrame contenant les données de la saison 2014/2015

# 3. Sélectionner les features et la cible dans df_train
features = [
    'points', 'goal_diff', 'buts_marques', 'buts_encaisses', 'victoires',
    'nuls', 'defaites', 'forme_5_derniers', 'matchs_dom', 'matchs_ext', 
    'adversaires_restants_avg_rank'
]

# 4. Entraînement (train)
X_train = df_train[features]
y_train = df_train['rank_final']  # Ou toute autre colonne cible que tu utilises

# 5. Test (test)
X_test = df_test[features]
y_test = df_test['rank_final']
# 3. Normaliser les données (optionnel mais souvent utile pour la régression linéaire)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# 5. Prédire les classements
y_pred = model.predict(X_test_scaled)

# 6. Ajouter les classements prédits au dataframe de test
df_test = X_test.copy()
df_test['rank_final_pred'] = y_pred

# 7. Ajouter la colonne "classement final" dans le même dataframe (si disponible dans df_test)
df_test['rank_final_actual'] = y_test.values

# 8. Afficher les résultats
# Ajouter une colonne pour l'ID ou le nom de l'équipe dans le DataFrame df_test

df_test['error'] = df_test['rank_final_actual'] - df_test['rank_final_pred']  # Erreur entre prédiction et réel
df_test_sorted = df_test.sort_values(by='rank_final_pred')  # Trier par classement prédit pour visualiser l'ordre

print(df_test_sorted[['rank_final_actual', 'rank_final_pred', 'error']])
