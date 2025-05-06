import csv

def ecart_de_buts(match):
    try:
        return abs(int(match["home_team_goal"]) - int(match["away_team_goal"]))
    except:
        return -1

def matchs_plus_grosse_diff(saison, league_id):
    teams = {}
    with open("data/Team.csv", newline='', encoding='utf-8') as f_teams:
        reader = csv.DictReader(f_teams)
        for row in reader:
            teams[row['team_api_id']] = row['team_long_name']
    with open("data/Match.csv", newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        max_diff = -1
        matchs_max = []

        # Recherche des matchs avec la plus grande différence de buts pour la saison et le league_id donnés
        for row in reader:
            if row.get("season") != saison or row.get("league_id") != str(league_id):
                continue

            diff = ecart_de_buts(row)

            if diff > max_diff:
                max_diff = diff
                matchs_max = [row]
            elif diff == max_diff:
                matchs_max.append(row)

        # Affichage du résultat
        print(f"Lors de la Saison : {saison}, En  : {(league_id)} | l'écart maximal de buts était : {max_diff}\n")
        for m in matchs_max:
            home_team_name = teams.get(m['home_team_api_id'], 'Inconnu')
            away_team_name = teams.get(m['away_team_api_id'], 'Inconnu')
            print(f"{home_team_name} {m['home_team_goal']} - {m['away_team_goal']} {away_team_name} ")


# Exemple d'appel de la fonction
matchs_plus_grosse_diff("2014/2015", 21518)
