from fonction_commune_chahid import *
from APS import process_player_attributes,moyenne
import math
import pandas as pd
# Charger les données
A=process_player_attributes("data/Player_Attributes.csv")
valeurs_interdites_saison = ["2006/2007","2016/2017"]
A = A[~A["saison"].isin(valeurs_interdites_saison)] 
def f(saison,id):
    s=[g for g in A["saison"]]
    id1 =[g for g in A["player_api_id"]]
    n=[g for g in A["overall_rating"]]
    for i in range(len(s)):
        if not math.isnan(int(id)):
           if (s[i]==saison) and (int(id1[i])==int(id)):
              return n[i] 
import pandas as pd
match=pd.read_csv("data/Match.csv")
def get_average_titular_rating_per_team_per_season(match_df, ratings_df):
    # Assure que les noms de colonnes soient cohérents
    ratings_df = ratings_df.rename(columns={"saison": "season"})

    # Liste des colonnes de joueurs
    home_players_cols = [f"home_player_{i}" for i in range(1, 12)]
    away_players_cols = [f"away_player_{i}" for i in range(1, 12)]

    # Rassembler les lignes home
    home = match_df[["season", "home_team_api_id"] + home_players_cols].copy()
    home = home.melt(
        id_vars=["season", "home_team_api_id"],
        value_vars=home_players_cols,
        var_name="position",
        value_name="player_api_id"
    )
    home["team_api_id"] = home["home_team_api_id"]
    home = home[["season", "team_api_id", "player_api_id"]]

    # Rassembler les lignes away
    away = match_df[["season", "away_team_api_id"] + away_players_cols].copy()
    away = away.melt(
        id_vars=["season", "away_team_api_id"],
        value_vars=away_players_cols,
        var_name="position",
        value_name="player_api_id"
    )
    away["team_api_id"] = away["away_team_api_id"]
    away = away[["season", "team_api_id", "player_api_id"]]

    # Concaténer home et away
    all_players = pd.concat([home, away], ignore_index=True)

    # Supprimer les joueurs manquants (parfois il peut y avoir des NaN)
    all_players = all_players.dropna(subset=["player_api_id"])

    # Convertir player_api_id en entier (si ce n'est pas déjà fait)
    all_players["player_api_id"] = all_players["player_api_id"].astype(int)

    # Merge avec les ratings
    merged = all_players.merge(
        ratings_df,
        on=["player_api_id", "season"],
        how="left"
    )

    # Moyenne de overall_rating par équipe et saison
    result = (
        merged.groupby(["team_api_id", "season"])["overall_rating"]
        .mean()
        .reset_index()
        .rename(columns={"overall_rating": "moyenne_overall_titulaire"})
    )

    return result
get_average_titular_rating_per_team_per_season(match, A).to_excel("titulaire.xlsx", index=False)
'''
def exo(season):
    match = lire_csv("data/Match.csv")
    player = lire_csv("data/Player.csv")
    team = lire_csv("data/Team.csv")
    match = match[(match["goal"].notna()) & (match["goal"] != "")]
    match = match[match["season"] == season]
    goals_transformed = [transforme(g) for g in match["goal"]]

    d = {}

    for goal in goals_transformed:
        if ("team" in goal.columns) and ("player1" in goal.columns):
            colonne_team = [g for g in goal["team"]]
            colonne_player1 = [g for g in goal["player1"]]
            for i in range(len(colonne_team)):
                if colonne_team[i] not in d:
                    d[str(colonne_team[i])] = []
                d[str(colonne_team[i])].append(colonne_player1[i])
    
    for e in d:
        d[e]=list(set(d[e]))
    for e in d:
        d[e][:]  =pd.Series(d[e]).dropna().tolist()
    for e in d:
        for i in range(len(d[e])):
             d[e][i]=(f(season,d[e][i]))
    for e in d:
        d[e]=moyenne(d[e])
    #print(d)
    return d

A1 = exo("2008/2009")  # d doit être retourné par la fonction exo
d1 = pd.DataFrame(list(A1.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d1["saison"] = "2008/2009"
#d1.to_excel('attribut_buteur1.xlsx', index=False)
A2 = exo("2009/2010")  # d doit être retourné par la fonction exo
d2 = pd.DataFrame(list(A2.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d2["saison"] = "2009/2010"
A3 = exo("2010/2011")  # d doit être retourné par la fonction exo
d3 = pd.DataFrame(list(A3.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d3["saison"] = "2010/2011"
A4 = exo("2011/2012")  # d doit être retourné par la fonction exo
d4 = pd.DataFrame(list(A4.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d4["saison"] = "2011/2012"
A5 = exo("2012/2013")  # d doit être retourné par la fonction exo
d5 = pd.DataFrame(list(A5.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d5["saison"] = "2012/2013" 
A6= exo("2013/2014")  # d doit être retourné par la fonction exo
d6 = pd.DataFrame(list(A6.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d6["saison"] = "2013/2014"
A7 = exo("2014/2015")  # d doit être retourné par la fonction exo
d7 = pd.DataFrame(list(A7.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d7["saison"] = "2014/2015"
A8 = exo("2015/2016")  # d doit être retourné par la fonction exo
d8 = pd.DataFrame(list(A8.items()), columns=["team_api_id", "moyenne_attributs_buteur"])
d8["saison"] = "2015/2016"
 
attribut_buteur = pd.concat([d1, d2, d3,d4,d5,d6,d7,d8], ignore_index=True)
age_buteur=pd.read_pickle('age_buteur.pkl')
attribut_passeur=pd.read_pickle('attribut_passeur.pkl')
age_passeur=pd.read_pickle('age_passeur.pkl')
but_tircadre= pd.read_pickle('but_tircadre.pkl')
tircadre_tirnoncadre=pd.read_pickle('tircadre_tirnoncadre.pkl')
final1= pd.merge(attribut_buteur, attribut_passeur, on=['team_api_id', 'saison'], how='outer')
final2=pd.merge(final1, age_buteur, on=['team_api_id', 'saison'], how='outer')
final3=pd.merge(final2, age_passeur, on=['team_api_id', 'saison'], how='outer')
final4=pd.merge(final3, but_tircadre, on=['team_api_id', 'saison'], how='outer')
Last_dance=pd.merge(final4, tircadre_tirnoncadre, on=['team_api_id', 'saison'], how='outer')
print(Last_dance)
'''
#print(f("2013/2014",150236))