



from fonctions_utiles_panda import transforme
import csv
from collections import defaultdict
import tkinter as tk
from tkinter import ttk

# Dictionnaire pour stocker les noms des équipes
team_names = {}
match = {}

#print(transforme("""<shoton><value><stats><blocked>1</blocked></stats><event_incident_typefk>61</event_incident_typefk><elapsed>4</elapsed><subtype>blocked_shot</subtype><player1>24211</player1><sortorder>1</sortorder><team>8456</team><n>216</n><type>shoton</type><id>452743</id></value><value><stats><blocked>1</blocked></stats><event_incident_typefk>61</event_incident_typefk><elapsed>4</elapsed><subtype>blocked_shot</subtype><player1>33963</player1><sortorder>3</sortorder><team>8456</team><n>217</n><type>shoton</type><id>452745</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>147</event_incident_typefk><elapsed>17</elapsed><subtype>shot</subtype><player1>24208</player1><sortorder>1</sortorder><team>8456</team><n>228</n><type>shoton</type><id>452770</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>311</event_incident_typefk><elapsed>28</elapsed><subtype>deflected</subtype><player1>33974</player1><sortorder>0</sortorder><team>8456</team><n>238</n><type>shoton</type><id>452790</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>135</event_incident_typefk><elapsed>35</elapsed><subtype>shot</subtype><player1>34574</player1><sortorder>1</sortorder><team>10261</team><n>245</n><type>shoton</type><id>452808</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>137</event_incident_typefk><elapsed>46</elapsed><subtype>distance</subtype><player1>24213</player1><sortorder>1</sortorder><team>8456</team><n>267</n><type>shoton</type><id>452843</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>137</event_incident_typefk><elapsed>61</elapsed><subtype>distance</subtype><player1>39027</player1><sortorder>1</sortorder><team>8456</team><n>284</n><type>shoton</type><id>452871</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>148</event_incident_typefk><elapsed>63</elapsed><subtype>header</subtype><player1>37799</player1><sortorder>1</sortorder><team>10261</team><n>286</n><type>shoton</type><id>452878</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>314</event_incident_typefk><elapsed>70</elapsed><subtype>deflected</subtype><player1>107216</player1><sortorder>0</sortorder><team>8456</team><n>292</n><type>shoton</type><id>452893</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>137</event_incident_typefk><elapsed>76</elapsed><subtype>distance</subtype><player1>33974</player1><sortorder>0</sortorder><team>8456</team><n>299</n><type>shoton</type><id>452911</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>137</event_incident_typefk><elapsed>84</elapsed><subtype>distance</subtype><player1>24213</player1><sortorder>0</sortorder><team>8456</team><n>307</n><type>shoton</type><id>452925</id></value><value><stats><shoton>1</shoton></stats><event_incident_typefk>137</event_incident_typefk><elapsed>88</elapsed><subtype>distance</subtype><player1>39027</player1><sortorder>0</sortorder><team>8456</team><n>309</n><type>shoton</type><id>452929</id></value></shoton>"""))


# Chargement des noms des équipes
with open("data/Team.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        team_id = int(row["team_api_id"])
        team_name = row["team_long_name"]
        team_names[team_id] = team_name
with open("data/Match.csv", mode="r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["season"] == "2014/2015" and row["league_id"] == "21518":
            match_id = int(row["match_api_id"])
            tir_cadre = row["shoton"]
            id_domicile = int(row["home_team_api_id"])
            id_exterieur = int(row["away_team_api_id"])
            but_domicile = row["home_team_goal"]
            but_exterieur = row["away_team_goal"]
            match[match_id] = [
            id_domicile,
            id_exterieur,
            but_domicile,
            but_exterieur,
            tir_cadre,
        ]
for e in match :
    if not isinstance(match[e][4], int):
        if match[e][4]=='':
            match[e][4]=1
        else:
            if len(transforme(match[e][4]))==0:
                match[e][4]=1
            else:
                match[e][4]=len(transforme(match[e][4]))


final = {}
for equipe in team_names:
    for matchs in match:
        if equipe == match[matchs][0]:
            if team_names[equipe] not in final:
                final[team_names[equipe]] = []
            final[team_names[equipe]].append((int(match[matchs][2])+int(match[matchs][3]))/int(match[matchs][4]))                

def moyenne(L):
    cpt = 0
    for i in range(len(L)):
        cpt += L[i] / len(L)
    return cpt


for e in final:
    final[e] = moyenne(final[e])
def min(A):
    cpt=A[0]
    for i in range(len(A)):
        if cpt<=A[i]:
            cpt=A[i]
    return cpt
C=[]
for e in final:
    C.append(final[e])
for e in final:
    if final[e]==min(C):
        print(e) 

