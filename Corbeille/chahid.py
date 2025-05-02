# Code de Chahid

# Classement des meilleurs buteurs, passeurs carton jaune, carton rouge
import xml.etree.ElementTree as ET
import pandas as pd

xml_data = """<card><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>73</event_incident_typefk><elapsed>18</elapsed><card_type>y</card_type><subtype>serious_fouls</subtype><player1>24970</player1><sortorder>2</sortorder><team>8600</team><n>253</n><type>card</type><id>950085</id></value><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>73</event_incident_typefk><elapsed>41</elapsed><card_type>y</card_type><subtype>serious_fouls</subtype><player1>33706</player1><sortorder>1</sortorder><team>8600</team><n>278</n><type>card</type><id>950166</id></value><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>73</event_incident_typefk><elapsed>57</elapsed><card_type>y</card_type><subtype>serious_fouls</subtype><player1>109298</player1><sortorder>1</sortorder><team>8600</team><n>299</n><type>card</type><id>950295</id></value><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>73</event_incident_typefk><elapsed>59</elapsed><card_type>y</card_type><subtype>serious_fouls</subtype><player1>30721</player1><sortorder>1</sortorder><team>8564</team><n>304</n><type>card</type><id>950308</id></value><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>73</event_incident_typefk><elapsed>79</elapsed><card_type>y</card_type><subtype>serious_fouls</subtype><player1>41694</player1><sortorder>4</sortorder><team>8600</team><n>335</n><type>card</type><id>950409</id></value></card>"""

root = ET.fromstring(xml_data)

# Extraire les données
data = []
for value in root.findall("value"):
    entry = {
        child.tag: child.text for child in value if child.tag != "stats"
    }  # Exclure stats pour l'instant
    stats = value.find("stats")  # Extraire les stats
    if stats is not None:
        entry.update({f"stats_{child.tag}": child.text for child in stats})
    data.append(entry)

# Convertir en DataFrame
df = pd.DataFrame(data)

# Afficher le résultat
print(df.columns)
df.to_csv("buts_match.csv", index=False, sep=",")
