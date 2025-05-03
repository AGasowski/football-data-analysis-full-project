import pandas as pd
from fonctions_communes import lire_csv

# ──────── FONCTIONS MAISON ────────


def nettoyer_attributs_techniques(df, colonnes):
    """Supprime les lignes avec des valeurs manquantes sur les attributs techniques."""
    return df.dropna(subset=colonnes)


def calculer_ecart_type_technique_par_joueur(df, colonnes):
    """Ajoute une colonne 'tech_std' : écart-type des attributs techniques par ligne."""
    df["tech_std"] = df[colonnes].std(axis=1)
    return df


def moyenne_ecart_type_par_joueur(df):
    """Calcule la moyenne des écarts-types pour chaque joueur."""
    return df.groupby("player_api_id")["tech_std"].mean().reset_index()


def construire_compteur_joueurs(matches):
    """Construit un dictionnaire : club → nombre d’apparitions de chaque joueur."""
    club_player_counts = {}
    for _, row in matches.iterrows():
        home_team = row["home_team_api_id"]
        away_team = row["away_team_api_id"]

        # Initialisation
        if home_team not in club_player_counts:
            club_player_counts[home_team] = {}
        if away_team not in club_player_counts:
            club_player_counts[away_team] = {}

        for i in range(1, 12):
            hp = row[f"home_player_{i}"]
            ap = row[f"away_player_{i}"]

            if pd.notna(hp):
                if hp not in club_player_counts[home_team]:
                    club_player_counts[home_team][hp] = 0
                club_player_counts[home_team][hp] += 1

            if pd.notna(ap):
                if ap not in club_player_counts[away_team]:
                    club_player_counts[away_team][ap] = 0
                club_player_counts[away_team][ap] += 1

    return club_player_counts


def extraire_top_joueurs_par_club(compteur, top_n=11):
    """Extrait les top N joueurs les plus utilisés pour chaque club."""
    club_player_pairs = []
    for club_id, joueurs in compteur.items():
        joueurs_tries = sorted(
            joueurs.items(), key=lambda x: x[1], reverse=True
        )[:top_n]
        for player_id, _ in joueurs_tries:
            club_player_pairs.append((club_id, player_id))
    return pd.DataFrame(
        club_player_pairs, columns=["team_api_id", "player_api_id"]
    )


def calculer_consistance_club(df_players, player_std_by_player, teams):
    """Calcule la moyenne des écarts-types pour chaque club, et ajoute le nom du club."""
    merged = df_players.merge(player_std_by_player, on="player_api_id")
    club_consistency = (
        merged.groupby("team_api_id")["tech_std"].mean().reset_index()
    )
    club_consistency = club_consistency.merge(
        teams[["team_api_id", "team_long_name"]], on="team_api_id"
    )
    return club_consistency.sort_values("tech_std")


def afficher_top_clubs_regularite(df, top_n=10):
    """Affiche les top N clubs avec les joueurs les plus réguliers."""
    print(
        f"Top {top_n} clubs les plus réguliers (selon 11 joueurs les plus utilisés) :"
    )
    print(df[["team_long_name", "tech_std"]].head(top_n))


# ──────── SCRIPT PRINCIPAL ────────

# Chargement
player_attr = lire_csv("data/Player_Attributes.csv")
matches = lire_csv("data/Match.csv")
teams = lire_csv("data/Team.csv")

# Attributs techniques utilisés
tech_attrs = [
    "ball_control",
    "short_passing",
    "long_passing",
    "dribbling",
    "vision",
    "finishing",
    "crossing",
]

# Traitement
player_attr = nettoyer_attributs_techniques(player_attr, tech_attrs)
player_attr = calculer_ecart_type_technique_par_joueur(player_attr, tech_attrs)
player_std_by_player = moyenne_ecart_type_par_joueur(player_attr)

compteur = construire_compteur_joueurs(matches)
club_player_df = extraire_top_joueurs_par_club(compteur)
club_consistency = calculer_consistance_club(
    club_player_df, player_std_by_player, teams
)

# Affichage
afficher_top_clubs_regularite(club_consistency)
