from fonction_commune_chahid import *


def diversite(season):
    # Charger les données
    match = lire_csv("data/Match.csv")
    player = lire_csv(
        "data/Player.csv"
    )  # Non utilisé ici, mais gardé pour usage potentiel
    team = lire_csv("data/Team.csv")  # Non utilisé ici non plus

    # Filtrer les matchs avec buts et la saison désirée
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == season]

    # Transformer la colonne "goal"
    goals_df = [transforme(g) for g in match["goal"]]

    # Dictionnaire pour stocker les buteurs et passeurs par équipe
    team_players = defaultdict(lambda: [set(), set()])  # [buteurs, passeurs]

    for df in goals_df:
        if "team" in df.columns and "player1" in df.columns and "player2" in df.columns:
            for _, row in df.iterrows():
                team_id = str(row["team"])
                if pd.notna(row["player1"]):
                    team_players[team_id][0].add(row["player1"])
                if pd.notna(row["player2"]):
                    team_players[team_id][1].add(row["player2"])

    # Préparer les résultats dans une liste
    results = []
    for team_id, (scorers, assisters) in team_players.items():
        nb_scorers = len(scorers)
        nb_assisters = len(assisters)
        nb_unique = len(scorers.union(assisters))

        results.append(
            {
                "team_api_id": int(team_id),
                "season": season,
                "nb_scorers": nb_scorers,
                "nb_assisters": nb_assisters,
                "nb_unique_contributors": nb_unique,
            }
        )

    return pd.DataFrame(results)


def diversite_toute_saison():
    # Charger les données
    match = lire_csv("data/Match.csv")

    # Extraire la liste unique des saisons
    saisons = match["season"].dropna().unique()

    # Générer les statistiques pour chaque saison
    all_stats = []
    for saison in saisons:
        df_saison = diversite(saison)
        all_stats.append(df_saison)

    # Concaténer tous les résultats
    df_final = pd.concat(all_stats, ignore_index=True)

    return df_final
