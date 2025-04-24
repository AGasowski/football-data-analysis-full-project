import pandas as pd
import locale
import platform


def lire_csv(chemin):
    return pd.read_csv(chemin)


def convertir_date(df):
    df["date"] = pd.to_datetime(df["date"])
    return df


def date_francais():
    """Configure la locale en français, compatible Windows, Linux et macOS."""
    systeme = platform.system()

    try:
        if systeme == "Windows":
            locale.setlocale(locale.LC_TIME, "French_France.1252")
        else:  # Linux ou macOS
            locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    except locale.Error:
        print(
            "⚠️ Impossible de définir la locale française. Elle n’est "
            "peut-être pas installée sur ce système."
        )
