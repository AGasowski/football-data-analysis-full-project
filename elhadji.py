import pandas as pd
#Classement des meilleurs buteurs dans toute l'europe ( allez disons qu'on va faire le top 30 des meilleus buteurs )
#tous championnats confondus : on aura donc besoin des tables match et player 

# on importe la table match 
fichier_source1 = "data/Match.csv"
match = pd.read_csv(fichier_source1) 

#On importe la table player 
fichier_source2 ="data/Player.csv"
player = pd.read_csv(fichier_source2)

# On commence d'abord a faire un classement pour la saison 2008/2009 pour la bundesliga 

#Reduisons tout de méme la table match pour garder que les match de bundesliga
# En regardant la table league , on voit que le country id de la bundesliga vaut 7809 et donc on peut maintenant restreindre :

 match = match[match["country_id"] == 7809]

#la colonne goal dans la table match a des elements qui sont eux meme des tables donc on va les stocker dans une liste L 
L=[]
for valeur in match["goal"]:
    L.append(valeur)
#Ainsi chaque element de la liste L correpond aux buts marqués pour un match de bundesliga . 
#Donc l'idée ici est de créer un dictionnaire donc les clés seront les id des joueurs ayant marqués
# Et pour chaque clé , sa valeur sera le nombre de but marqué . 

d={}
for i in range(len(L)):
   #On parcourt les elements de la liste L , qui sont des tables de matchs 
   for nom_joueur in L[i]["player1"]:
      #On s'interesse a la colonne Player1 de la table dont on parcours ( je ne sais pas si c'est le bon attribut)
      #j'ai supposé que c'est le player 1 qui a marqué le but : on demandra au prof demain .
      if nom_joueur not in d:
         #si le joeur n'est pas dans le dictionnaire , donc c'est la premiere fois qu'il marque alors on lui rajoute juste 1 but 
         d["nom_joeur"]=1
      else:
         #si le joueur est deja dans le dictionnaire , il avait donc deja marqué et on ajoute alors de 1 son nb de but
         d["nom_joeur"] +=1  

#Donc la le dictionnaire a les gens qui ont marqués et leurs nombres de buts 
#on va ainsi faire le lien avec la table player pour avoir le lien avec le nom des joeurs ( bien sur que le classement viendra apres )
# Je m'interesse a la table player et je vais garder que les colonnes : player_api_id et player_name 
player=player[["player_api_id","player_name"]]
#Ainsi je veux que les joueurs qui ont marqué dans ma table donc je dois utiliser mon dictionnaire 
player = player[player["player_api_id"].isin(d())]
# il reste juste a ajouter une nouvelle colonne que l'on va appeler but , et on utilise les valeurs des dictionnaire 




