import pandas as pd
import locale
import platform


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
    Configure la locale en français, compatible Windows, Linux et macOS. Ne pas
    ajouter au code car elle est déjà incluse dans la fonction convertir_date()
    """
    systeme = platform.system()

    try:
        if systeme == "Windows":
            locale.setlocale(locale.LC_TIME, "French_France.1252")
        else:  # Linux ou macOS
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        print(
            "Impossible de définir la locale française. Elle n’est "
            "peut-être pas installée sur ce système."
        )
