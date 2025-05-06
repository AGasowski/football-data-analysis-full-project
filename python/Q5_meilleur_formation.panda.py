from fonctions_communes import (
    lire_csv,
    select_all,
    diff_abs,
    formation,
    convertir_list,
)  
from Corbeille.fonction_commune_elhadji import (fusionner_colonnes_en_listes,cle_maximale,)

match = lire_csv("data/Match.csv")
match = select_all(match, "season", "2014/2015")
match = select_all(match ,"league_id",21518)
player = lire_csv("data/Match.csv") 
 
Coordonée_home_joueur = fusionner_colonnes_en_listes(match, ["home_player_Y2","home_player_Y3","home_player_Y4","home_player_Y5","home_player_Y6","home_player_Y7","home_player_Y8","home_player_Y9","home_player_Y10","home_player_Y11"]) 
Coordonée_away_joueur = fusionner_colonnes_en_listes(match,["away_player_Y2","away_player_Y3","away_player_Y4","away_player_Y5","away_player_Y6","away_player_Y7","away_player_Y8","away_player_Y9","away_player_Y10","away_player_Y11"])
match["ecart"]=diff_abs(match, "home_team_goal", "away_team_goal")
diff_but = convertir_list (match,"ecart") 



d = {}
for i in range(len(Coordonée_home_joueur)):

        if tuple(formation(Coordonée_home_joueur[i])) not in d : 
            d[tuple(formation(Coordonée_home_joueur[i]))] = 1
        else:
            d[tuple(formation(Coordonée_home_joueur[i]))] += 1

        if tuple(formation(Coordonée_away_joueur[i])) not in d:
            d[tuple(formation(Coordonée_away_joueur[i]))] = 1
        else:
            d[tuple(formation(Coordonée_away_joueur[i]))] += 1  

classement = sorted(d.items(), key=lambda item: item[1], reverse=True)
for rang, (formation, nb_occurrences) in enumerate(classement, start=1):
    print(f"{rang}.  {formation} - {nb_occurrences} fois")
#print(cle_maximale(d))  



