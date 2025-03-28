# Code de Chahid

# Classement des meilleurs buteurs, passeurs carton jaune, carton rouge
import xml.etree.ElementTree as ET
import pandas as pd
xml_data = """<goal><value><comment>n</comment><stats><goals>1</goals><shoton>1</shoton></stats><event_incident_typefk>406</event_incident_typefk><coordinates><value>25</value><value>62</value></coordinates><elapsed>9</elapsed><player2>409193</player2><subtype>header</subtype><player1>354491</player1><sortorder>1</sortorder><team>6391</team><id>5164497</id><n>95</n><type>goal</type><goal_type>n</goal_type></value><value><comment>n</comment><stats><goals>1</goals><shoton>1</shoton></stats><event_incident_typefk>393</event_incident_typefk><coordinates><value>20</value><value>63</value></coordinates><elapsed>31</elapsed><player2>466143</player2><subtype>shot</subtype><player1>208676</player1><sortorder>2</sortorder><team>6391</team><id>5164787</id><n>264</n><type>goal</type><goal_type>n</goal_type></value><value><comment>p</comment><stats><penalties>1</penalties><goals>1</goals></stats><event_incident_typefk>20</event_incident_typefk><coordinates><value>23</value><value>8</value></coordinates><elapsed>51</elapsed><player1>359188</player1><sortorder>0</sortorder><team>9829</team><id>5165289</id><n>346</n><type>goal</type><goal_type>p</goal_type></value><value><comment>n</comment><stats><goals>1</goals><shoton>1</shoton></stats><event_incident_typefk>406</event_incident_typefk><coordinates><value>19</value><value>7</value></coordinates><elapsed>74</elapsed><player2>29590</player2><subtype>header</subtype><player1>30911</player1><sortorder>1</sortorder><team>9829</team><id>5165682</id><n>520</n><type>goal</type><goal_type>n</goal_type></value></goal>"""

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
print(df['subtype'])
df.to_csv("buts_match.csv", index=False, sep=",")
