### Code de Chahid

## Classement des meilleurs buteurs, passeurs carton jaune, carton rouge
import xml.etree.ElementTree as ET
import pandas as pd
xml_data = """<goal>
<value><comment>n</comment><stats><goals>1</goals><shoton>1</shoton></stats>
<event_incident_typefk>406</event_incident_typefk><elapsed>51</elapsed>
<player2>24773</player2><subtype>header</subtype><player1>38899</player1>
<sortorder>2</sortorder><team>10194</team><id>1342832</id><n>476</n>
<type>goal</type><goal_type>n</goal_type></value>
<value><comment>n</comment><stats><goals>1</goals><shoton>1</shoton></stats>
<elapsed_plus>3</elapsed_plus><event_incident_typefk>393</event_incident_typefk>
<elapsed>90</elapsed><player2>38755</player2><subtype>shot</subtype>
<player1>47418</player1><sortorder>2</sortorder><team>10194</team>
<id>1343383</id><n>532</n><type>goal</type><goal_type>n</goal_type></value>
</goal>"""

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
