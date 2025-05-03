from fonction_commune_chahid import *
from APA_diversite import *
from APA_Carton_rouge import *

diversite_df = diversite_toute_saison()
table_chahid = fusionner(
    carton_df, diversite_df, ["team_api_id", "season"], ["team_api_id", "season"]
)

print(table_chahid)
