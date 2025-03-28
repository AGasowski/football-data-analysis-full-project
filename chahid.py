# Code de Chahid

# Classement des meilleurs buteurs, passeurs carton jaune, carton rouge
import xml.etree.ElementTree as ET
import pandas as pd
xml_data = """<card><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>73</event_incident_typefk><elapsed>56</elapsed><card_type>y</card_type><subtype>serious_fouls</subtype><player1>37442</player1><sortorder>5</sortorder><team>8650</team><n>327</n><type>card</type><id>377978</id></value><value><comment>y</comment><stats><ycards>1</ycards></stats><event_incident_typefk>25</event_incident_typefk><elapsed>90</elapsed><card_type>y</card_type><subtype>stall_time</subtype><player1>46621</player1><sortorder>3</sortorder><team>8650</team><n>353</n><type>card</type><id>378060</id></value></card>"""

root = ET.fromstring(xml_data)

# Extraire les données
data = []
for value in root.findall("value"):
    entry = {child.tag: child.text for child in value if child.tag != "stats"}  # Exclure stats pour l'instant
    stats = value.find("stats")  # Extraire les stats
    if stats is not None:
        entry.update({f"stats_{child.tag}": child.text for child in stats})
    data.append(entry)

# Convertir en DataFrame
df = pd.DataFrame(data)

# Afficher le résultat
print(df)
df.to_csv("buts_match.csv", index=False, sep=",")
