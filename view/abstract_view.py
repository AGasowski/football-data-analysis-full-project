"""
Module 'view.py'

Ce module contient des classes représentant différentes vues pour une interface
utilisateur, y compris une vue console et une vue graphique utilisant Tkinter.
La classe abstraite `AbstractView` définit l'interface de base pour ces vues.
Chaque sous-classe doit implémenter les méthodes `display_info` et
`make_choice` pour offrir des comportements spécifiques d'affichage et
d'interaction avec l'utilisateur.
"""

from abc import ABC


class AbstractView(ABC):
    """
    Classe abstraite représentant une vue générale de l'application.

    Cette classe sert de base pour des vues spécifiques, telles que la vue
    console ou la vue graphique. Elle contient des styles prédéfinis pour
    l'interface et des méthodes abstraites que les sous-classes doivent
    implémenter afin de personnaliser l'affichage et l'interaction avec
    l'utilisateur.

    """

    def __init__(self):
        self.style = {
            "separator": "ffffff",
            "questionmark": "000000",
            "selected": "00BFFF",
            "pointer": "ffffff",
            "instruction": "ffffff",
            "answer": "008000",
            "question": "FF7F50",
        }
