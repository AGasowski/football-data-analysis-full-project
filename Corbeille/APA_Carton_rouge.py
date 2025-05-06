from fonction_commune_chahid import *


def carton(season, couleur):  # couleur : str
    # Charger les données
    match = lire_csv("data/Match.csv")
    player = lire_csv(
        "data/Player.csv"
    )  # Pas utilisé ici mais conservé si besoin futur

    # Filtrer les matchs avec des événements de buts et la bonne saison
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == season]

    # Extraire les données de cartons
    card_df_list = [transforme(g) for g in match["card"]]

    # Initialiser le dictionnaire des statistiques
    team_stats = creer_dict(2)  # {team_id: [nb_cartons_rouges, nb_matchs]}

    if "home_team_api_id" in match.columns and "away_team_api_id" in match.columns:
        for _, row in match.iterrows():
            home = str(row["home_team_api_id"])
            away = str(row["away_team_api_id"])
            team_stats[home][1] += 1
            team_stats[away][1] += 1

    for df in card_df_list:
        if "team" in df.columns and "card_type" in df.columns:
            cards = df[df["card_type"] == couleur]
            for team in cards["team"]:
                team_stats[str(team)][0] += 1

    # Construire la liste de résultats
    results = []
    for team_id, (nb_cards, nb_matches) in team_stats.items():
        ratio = round(nb_cards / nb_matches, 2) if nb_matches > 0 else 0
        results.append(
            {
                "team_api_id": int(team_id),
                "season": season,
                f"{couleur}_cards_per_match": ratio,
                "match_count": nb_matches,
            }
        )

    # Retourner un DataFrame
    return pd.DataFrame(results)


def carton_toute_saison(couleur):
    # Charger les données
    match = lire_csv("data/Match.csv")

    # Extraire la liste unique des saisons
    saisons = match["season"].dropna().unique()

    # Générer les statistiques pour chaque saison
    all_stats = []
    for saison in saisons:
        df_saison = carton(saison, couleur)
        all_stats.append(df_saison)

    # Concaténer tous les résultats
    df_final = pd.concat(all_stats, ignore_index=True)

    return df_final


carton_jaune_df = carton_toute_saison("y")
carton_rouge_df = carton_toute_saison("r")
carton_df = fusionner(
    carton_jaune_df,
    carton_rouge_df,
    ["team_api_id", "season"],
    ["team_api_id", "season"],
)
