import pandas as pd
import datetime
import locale
import platform
import pytest
from src.fonctions.dates_formats import (
    convertir_date,
    date_format,
    convertir_col_date,
    date_francais,
)


def test_convertir_date():
    df = pd.DataFrame({"date": ["2024-01-01", "2024-02-01"]})
    result = convertir_date(df)
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_date_format():
    date = datetime.datetime(2024, 1, 1)
    resultat = date_format(date)
    assert isinstance(resultat, str)
    # On ne teste pas la valeur exacte car elle dépend de la locale installée


def test_convertir_col_date():
    df = pd.DataFrame(
        {"evenement": ["x", "y"], "timestamp": ["2023-10-10", "2024-01-01"]}
    )
    result = convertir_col_date(df, "timestamp")
    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])


def test_date_francais_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    try:
        date_francais()
    except locale.Error:
        pass  # Si la locale n’est pas installée sur la machine de test


def test_date_francais_linux(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    try:
        date_francais()
    except locale.Error:
        pass  # Idem


def test_date_francais_erreur_locale(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    monkeypatch.setattr(
        locale,
        "setlocale",
        lambda *args, **kwargs: (_ for _ in ()).throw(locale.Error("erreur")),
    )
    try:
        date_francais()
    except Exception:
        pytest.fail(
            "La fonction ne devrait pas lever d'exception même si la locale"
            " échoue."
        )
