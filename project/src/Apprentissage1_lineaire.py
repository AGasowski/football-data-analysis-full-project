"""
Ce module entraîne un modèle de régression linéaire pour prédire le classement
d'une équipe de football à partir de statistiques de matchs et d'équipes.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import (
    LinearRegression,
)  # Utilisation de LinearRegression
from sklearn.preprocessing import StandardScaler
from project.src.fonctions.manipulations import fusionner, id_to_nom
from project.src.fonctions.statistiques import calculer_classement


def predire_classement_avec_confiance(saison, league_id_cible, team_id_cible):
    """
    Prédit le classement d'une équipe pour une saison donnée à l'aide
    d'un modèle de régression linéaire, et retourne son rang et un intervalle
    de confiance sur ses points.

    Args:
        saison (str): Saison cible (ex: "2014/2015")
        league_id_cible (int): ID de la ligue
        team_id_cible (int): ID de l'équipe

    Retour : - None. Les résultats sont affichés dans la console.
    """

    # Chargement des données
    df_equipe = pd.read_excel("stats_equipes.xlsx")
    df_titulaire = pd.read_excel("titulaire.xlsx")
    df_match = pd.read_excel("match.xlsx")

    # Fusion
    df_equipe = fusionner(
        df_equipe,
        df_titulaire,
        ["team_api_id", "saison"],
        ["team_api_id", "season"],
    )

    # Jointures home
    df_match = df_match.merge(
        df_equipe,
        left_on=["home_team_api_id", "saison"],
        right_on=["team_api_id", "saison"],
        how="left",
        suffixes=("", "_h"),
    )
    df_match = df_match.rename(
        columns=lambda x: (
            x + "_h"
            if x in df_equipe.columns and x not in ["team_api_id", "saison"]
            else x
        )
    )

    # Jointures away
    df_match = df_match.merge(
        df_equipe,
        left_on=["away_team_api_id", "saison"],
        right_on=["team_api_id", "saison"],
        how="left",
        suffixes=("", "_a"),
    )
    df_match = df_match.rename(
        columns=lambda x: (
            x + "_a"
            if x in df_equipe.columns and x not in ["team_api_id", "saison"]
            else x
        )
    )

    # Sélection des features
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

    df_match_clean = df_match.dropna()
    train = df_match_clean[df_match_clean["saison"] < "2014/2015"]
    test = df_match_clean[df_match_clean["saison"] == saison]

    x_train = train[features]
    y_train_home = train["home_team_goal"]
    y_train_away = train["away_team_goal"]
    x_test = test[features]

    # Standardisation
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # Modèle de régression linéaire
    linear_home = (
        LinearRegression()
    )  # Remplacer PoissonRegressor par LinearRegression
    linear_away = (
        LinearRegression()
    )  # Remplacer PoissonRegressor par LinearRegression

    linear_home.fit(x_train_scaled, y_train_home)
    linear_away.fit(x_train_scaled, y_train_away)

    # Prédictions
    pred_home = linear_home.predict(x_test_scaled)
    pred_away = linear_away.predict(x_test_scaled)

    # Simulation du classement avec points
    df_test = test.copy()
    classement = []

    for i, row in enumerate(df_test.itertuples()):
        id1 = row.home_team_api_id
        id2 = row.away_team_api_id
        league_id = row.league_id

        home_goals = round(pred_home[i])
        away_goals = round(pred_away[i])

        if home_goals > away_goals:
            points_home, points_away = 3, 0
        elif home_goals < away_goals:
            points_home, points_away = 0, 3
        else:
            points_home = points_away = 1

        classement.append(
            {
                "team_api_id": id1,
                "league_id": league_id,
                "points": points_home,
                "but_marques": home_goals,
                "but_encaisses": away_goals,
            }
        )
        classement.append(
            {
                "team_api_id": id2,
                "league_id": league_id,
                "points": points_away,
                "but_marques": away_goals,
                "but_encaisses": home_goals,
            }
        )

    df_classement = pd.DataFrame(classement)
    df_resultats = (
        df_classement.groupby(["league_id", "team_api_id"])
        .agg(
            points_total=("points", "sum"),
            buts_marques=("but_marques", "sum"),
            buts_encaisses=("but_encaisses", "sum"),
        )
        .reset_index()
    )

    # Trie pour obtenir le classement
    df_resultats = df_resultats.sort_values(
        ["league_id", "points_total"], ascending=[True, False]
    )
    df_resultats["rank"] = df_resultats.groupby("league_id")[
        "points_total"
    ].rank(method="first", ascending=False)
    df_resultats["team_api_id"] = df_resultats["team_api_id"].apply(id_to_nom)

    # Extraire le classement de l'équipe cible
    df_ligue = df_resultats[
        df_resultats["league_id"] == league_id_cible
    ].reset_index(drop=True)

    # Nom de l'équipe cible
    nom_equipe = id_to_nom(team_id_cible)

    # Vérifie si l'équipe est dans le classement de la ligue
    if nom_equipe not in df_ligue["team_api_id"].values:
        print(
            f"Pour la saison {saison}, l'équipe {nom_equipe} a été reléguée "
            f"ou n’a pas participé à cette ligue."
        )
        return None, None

    # Intervalle de confiance
    sigma_points = df_classement["points"].std()
    n_matchs = df_classement[
        df_classement["team_api_id"] == team_id_cible
    ].shape[0]
    erreur_type = sigma_points / np.sqrt(n_matchs)

    # Extraire les infos pour l'équipe cible
    ligne_equipe = df_ligue[df_ligue["team_api_id"] == nom_equipe].iloc[0]
    ic_inf = ligne_equipe["points_total"] - 1.96 * erreur_type
    ic_sup = ligne_equipe["points_total"] + 1.96 * erreur_type
    rang = ligne_equipe["rank"]
    # calcul de RMSE
    df_match = pd.read_csv("data/Match.csv")
    df_reel = calculer_classement(df_match, saison, league_id_cible)
    # Merge classement prédit et réel
    df_pred = df_ligue[["team_api_id", "rank"]].rename(
        columns={"rank": "classement_pred"}
    )
    df_reel["team_api_id"] = df_reel["team_api_id"].apply(id_to_nom)

    df_comparaison = df_pred.merge(df_reel, on="team_api_id")

    # Calcul du RMSE
    rmse = np.sqrt(
        (
            (df_comparaison["classement_pred"] - df_comparaison["rank"]) ** 2
        ).mean()
    )
    print(f"RMSE du modèle sur la saison {saison} : {rmse:.2f}")

    print(
        f"Pour la saison {saison}, l'équipe {nom_equipe} sera classée "
        f"{int(rang)}ᵉ avec un intervalle de confiance approximatif sur les "
        f"points de [{ic_inf:.2f}, {ic_sup:.2f}]."
    )
    return int(rang), (ic_inf, ic_sup)
