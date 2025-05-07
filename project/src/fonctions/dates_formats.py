"""
Module de gestion des dates avec formatage en français.

Ce module fournit des fonctions pour gérer les conversions et le formatage
de dates selon les conventions françaises. Il utilise le module `locale`
pour configurer l'affichage des dates en français, ainsi que le module
`datetime` pour la manipulation des dates.
"""

import locale
import platform
from datetime import datetime
import pandas as pd


# Gérer les conversions de dates et l’affichage selon la locale française.


# Conversion et formatage de dates
def convertir_date(df):
    """
    Convertit la colonne 'date' d'un DataFrame en format datetime, puis
    applique une configuration de date en français.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant une colonne 'date' sous forme de chaînes de
        caractères.

    Retourne
    -------
    pandas.DataFrame
        Le DataFrame avec la colonne 'date' convertie en datetime.
    """
    df["date"] = pd.to_datetime(df["date"])
    date_francais()
    return df


def date_format(date):
    """
    Formate une date en français avec le jour, le mois et l’année.

    Paramètres
    ----------
    date : datetime.datetime
        Date à formater.

    Retourne
    -------
    str
        Date formatée sous forme : 'lundi 01 janvier 2024'.
    """
    return date.strftime("%A %d %B %Y")


def convertir_col_date(df, colonne):
    """
    Convertit une colonne d'un DataFrame en format datetime.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame contenant la colonne à convertir.
    colonne : str
        Le nom de la colonne à convertir au format datetime.

    Retour
    ------
    pandas.DataFrame
        Le DataFrame original avec la colonne spécifiée convertie en datetime.

    """
    df[colonne] = pd.to_datetime(df[colonne])
    return df


# Gestion de la langue
def date_francais():
    """
    Configure la locale pour afficher les dates en français.
    """
    systeme = platform.system()
    try:
        if systeme == "Windows":
            locale.setlocale(locale.LC_TIME, "French_France.1252")
        else:
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        print("⚠️ Locale française non disponible sur ce système.")


def formater_date_fr(date_str):
    """
    Convertit une chaîne de date en datetime et la formate joliment en
    français.

    Args:
        date_str (str): Une chaîne de date ISO.

    Returns:
        str: Une date formatée du type 'samedi 13 septembre 2014'.
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%A %d %B %Y")
    except ValueError:
        return date_str  # Retourne la chaîne brute si erreur
