import pandas as pd
import numpy as np
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from project.src.fonctions.manipulations import id_to_nom

# Charger les données


def predire_classement_avec_confiance(saison, league_id_cible, team_id_cible):
    match = pd.read_csv("data/Match.csv")
    match = match[
        match["league_id"] == league_id_cible
    ]  # Filtrer la ligue souhaitée

    def extraire_caracteristiques_mi_saison(df_season):
        df_season = df_season[
            [
                "home_team_api_id",
                "away_team_api_id",
                "date",
                "home_team_goal",
                "away_team_goal",
            ]
        ].copy()
        df_season["date"] = pd.to_datetime(df_season["date"])

        equipes = pd.unique(
            df_season[["home_team_api_id", "away_team_api_id"]].values.ravel()
        )

        stats = []

        for team_id in equipes:
            matchs = (
                df_season[
                    (df_season["home_team_api_id"] == team_id)
                    | (df_season["away_team_api_id"] == team_id)
                ]
                .sort_values("date")
                .head(19)
            )

            points, goal_diff = 0, 0
            buts_marques, buts_encaisses = 0, 0
            victoires, nuls, defaites = 0, 0, 0
            dom, ext = 0, 0

            for _, row in matchs.iterrows():
                if row["home_team_api_id"] == team_id:
                    dom += 1
                    buts_marques += row["home_team_goal"]
                    buts_encaisses += row["away_team_goal"]
                    if row["home_team_goal"] > row["away_team_goal"]:
                        points += 3
                        victoires += 1
                    elif row["home_team_goal"] == row["away_team_goal"]:
                        points += 1
                        nuls += 1
                    else:
                        defaites += 1
                    goal_diff += row["home_team_goal"] - row["away_team_goal"]
                else:
                    ext += 1
                    buts_marques += row["away_team_goal"]
                    buts_encaisses += row["home_team_goal"]
                    if row["away_team_goal"] > row["home_team_goal"]:
                        points += 3
                        victoires += 1
                    elif row["away_team_goal"] == row["home_team_goal"]:
                        points += 1
                        nuls += 1
                    else:
                        defaites += 1
                    goal_diff += row["away_team_goal"] - row["home_team_goal"]

            # Forme des 5 derniers matchs
            forme = 0
            derniers = matchs.tail(5)
            for _, row in derniers.iterrows():
                if row["home_team_api_id"] == team_id:
                    if row["home_team_goal"] > row["away_team_goal"]:
                        forme += 3
                    elif row["home_team_goal"] == row["away_team_goal"]:
                        forme += 1
                else:
                    if row["away_team_goal"] > row["home_team_goal"]:
                        forme += 3
                    elif row["away_team_goal"] == row["home_team_goal"]:
                        forme += 1

            stats.append(
                {
                    "equipe": team_id,
                    "points": points,
                    "goal_diff": goal_diff,
                    "buts_marques": buts_marques,
                    "buts_encaisses": buts_encaisses,
                    "victoires": victoires,
                    "nuls": nuls,
                    "defaites": defaites,
                    "forme_5_derniers": forme,
                    "matchs_dom": dom,
                    "matchs_ext": ext,
                }
            )

        df_stats = pd.DataFrame(stats)
        df_stats = df_stats.sort_values(
            by=["points", "goal_diff"], ascending=False
        ).reset_index(drop=True)
        df_stats["rank"] = df_stats.index + 1
        return df_stats, df_season

    def calculer_rank_final(df_season, equipes):
        total_points = {}
        for team_id in equipes:
            pts = 0
            for _, row in df_season.iterrows():
                if row["home_team_api_id"] == team_id:
                    if row["home_team_goal"] > row["away_team_goal"]:
                        pts += 3
                    elif row["home_team_goal"] == row["away_team_goal"]:
                        pts += 1
                elif row["away_team_api_id"] == team_id:
                    if row["away_team_goal"] > row["home_team_goal"]:
                        pts += 3
                    elif row["away_team_goal"] == row["home_team_goal"]:
                        pts += 1
            total_points[team_id] = pts

        df_final = pd.DataFrame(
            list(total_points.items()), columns=["equipe", "points_fin_saison"]
        )
        df_final = df_final.sort_values(
            by="points_fin_saison", ascending=False
        ).reset_index(drop=True)
        df_final["rank_final"] = df_final.index + 1
        return df_final

    def ajouter_moyenne_rang_adversaires_restants(df_stats, df_season):
        rank_dict = df_stats.set_index("equipe")["rank"].to_dict()
        moyennes = []

        for team_id in df_stats["equipe"]:
            matchs = df_season[
                (df_season["home_team_api_id"] == team_id)
                | (df_season["away_team_api_id"] == team_id)
            ].sort_values("date")
            remaining = matchs.iloc[19:]
            opponents = [
                (
                    row["away_team_api_id"]
                    if row["home_team_api_id"] == team_id
                    else row["home_team_api_id"]
                )
                for _, row in remaining.iterrows()
            ]
            ranks = [
                rank_dict.get(oppo) for oppo in opponents if oppo in rank_dict
            ]
            moyennes.append(np.mean(ranks) if ranks else np.nan)

        df_stats["average_rank_remaining_opponents"] = moyennes
        return df_stats

    def preparer_donnees_saison(season):
        df_season = match[match["season"] == season]
        df_stats, df_season = extraire_caracteristiques_mi_saison(df_season)
        df_stats = ajouter_moyenne_rang_adversaires_restants(
            df_stats, df_season
        )
        df_rank_final = calculer_rank_final(df_season, df_stats["equipe"])
        df_result = df_stats.merge(df_rank_final, on="equipe")
        return df_result

    # Étape 3 : Créer un dataset combiné sur plusieurs saisons
    saisons = [
        "2008/2009",
        "2009/2010",
        "2010/2011",
        "2011/2012",
        "2012/2013",
        "2013/2014",
    ]
    df_all = pd.concat(
        [preparer_donnees_saison(s) for s in saisons], ignore_index=True
    )

    # Étape 4 : Préparer les données pour l'apprentissage
    features = [
        "points",
        "goal_diff",
        "buts_marques",
        "buts_encaisses",
        "victoires",
        "nuls",
        "defaites",
        "forme_5_derniers",
        "matchs_dom",
        "matchs_ext",
    ]

    X_train = df_all[features]
    y_train = df_all["rank_final"]

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Tester sur une autre saison
    df_test = preparer_donnees_saison(saison)
    X_test = df_test[features]
    y_test = df_test["rank_final"]
    X_test_scaled = scaler.transform(X_test)
    # rang mi saison
    df_rank = match[match["season"] == saison]
    df_rank1, _ = extraire_caracteristiques_mi_saison(df_rank)
    rang_mi_saison = df_rank1[df_rank1["equipe"] == team_id_cible][
        "rank"
    ].values[0]
    # Modèle de régression de Poisson
    model = PoissonRegressor()

    # Entraînement du modèle
    model.fit(X_train_scaled, y_train)

    # Prédiction avec le modèle de Poisson
    y_pred = model.predict(X_test_scaled)
    # Trouver l'index de l'équipe dans df_test
    index_team = df_test[df_test["equipe"] == team_id_cible].index[0]

    # Accéder à la prédiction pour cette équipe
    predicted_rank = y_pred[index_team]

    print(
        f"Pour la saison {saison}, l'équipe {id_to_nom(team_id_cible)} qui "
        f"était {rang_mi_saison}ᵉ a la mi-saison, sera classée "
        f"{predicted_rank.round().astype(int)}ᵉ en fin de saison "
    )
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE : {rmse:.2f}")


predire_classement_avec_confiance("2014/2015", 21518, 8633)
"""
# Comparaison des prédictions
df_comparaison = pd.DataFrame({
    "Équipe": df_test["equipe"],
    "Rang Réel": y_test.values,
    "Rang Prédit": y_pred.round().astype(int)
}).sort_values("Rang Réel")

print(df_comparaison.head(10))
"""
