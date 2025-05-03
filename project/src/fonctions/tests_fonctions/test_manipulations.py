import pytest
import pandas as pd
from collections import defaultdict
from manipulations import (
    filtrer_df,
    fusionner,
    id_championnat,
    creer_dict,
    name_team_dic,
    cles_dic,
    filtre_dic,
    ratio_dic,
    cle_extreme,
    appliquer_fonction_aux_valeurs,
)


@pytest.mark.parametrize(
    "df, filtre_col, filtre_val, colonnes, expected",
    [
        (
            pd.DataFrame({"A": [1, 2, 2], "B": ["x", "y", "z"]}),
            "A",
            2,
            ["B"],
            pd.Series(["y", "z"], index=[1, 2], name="B"),
        ),
    ],
)
def test_filtrer_df(df, filtre_col, filtre_val, colonnes, expected):
    result = filtrer_df(df, filtre_col, filtre_val, colonnes)
    pd.testing.assert_series_equal(result, expected)


def test_fusionner_basic():
    df1 = pd.DataFrame({"A": [1, 2, 3], "val1": ["a", "b", "c"]})
    df2 = pd.DataFrame({"B": [3, 1, 4], "val2": ["x", "y", "z"]})
    result = fusionner(df1, df2, "A", "B")
    expected = pd.DataFrame(
        {"A": [1, 3], "val1": ["a", "c"], "B": [1, 3], "val2": ["y", "x"]}
    )
    pd.testing.assert_frame_equal(result.reset_index(drop=True), expected)


@pytest.mark.parametrize(
    "nom, expected_id",
    [
        ("Tous les championnats réunis", 0),
        ("Ligue 1 (France)", 4769),
        ("Super League (Suisse)", 24558),
        ("Inexistant", None),
    ],
)
def test_id_championnat_varie(nom, expected_id):
    assert id_championnat(nom) == expected_id


def test_creer_dict_type_et_valeurs():
    d = creer_dict(3)
    assert isinstance(d, defaultdict)
    assert d["abc"] == [0, 0, 0]


def test_name_team_dic_typique():
    dic = {1: "PSG", 2: "OM"}
    assert name_team_dic(dic, 1) == "PSG"
    assert name_team_dic(dic, "2") == "OM"
    assert name_team_dic(dic, "x") == "Inconnu"


def test_cles_dic_contenu():
    d = {"a": 1, "b": 2}
    assert set(cles_dic(d)) == {"a", "b"}


def test_filtre_dic_filtrage_correct():
    d = {"a": [1, 2], "b": [3, 2], "c": [1, 5]}
    result = filtre_dic(d, 1, 2)
    assert result == {"a": [1, 2], "b": [3, 2]}


def test_ratio_dic_cas_divers():
    d = {"x": [10, 2]}
    assert ratio_dic(d, "x", 0, 1) == 5.0
    d["x"][1] = 0
    assert ratio_dic(d, "x", 0, 1) == 0


def test_cle_extreme_comportement():
    d = {"a": 1, "b": 5, "c": 3}
    assert cle_extreme(d, "max") == "b"
    assert cle_extreme(d, "min") == "a"
    with pytest.raises(ValueError):
        cle_extreme({}, "max")
    with pytest.raises(ValueError):
        cle_extreme({"a": 1}, "moyenne")


def test_appliquer_fonction_aux_valeurs_doublement():
    d = {"a": 1, "b": 2}
    result = appliquer_fonction_aux_valeurs(d, lambda x: x * 2)
    assert result == {"a": 2, "b": 4}
