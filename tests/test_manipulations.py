import pytest
import pandas as pd
from collections import defaultdict
from project.src.fonctions.manipulations import (
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
    creer_tranche_age,
    id_en_nom,
    get_saison,
    creer_colonne_age_au_moment,
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


def test_id_championnat_inconnu():
    assert id_championnat("Championnat Inconnu") is None


def test_id_en_nom_substitution():
    match_df = pd.DataFrame(
        {"home_team_api_id": [1, 2], "away_team_api_id": [2, 3]}
    )
    team_df = pd.DataFrame(
        {"team_api_id": [1, 2], "team_long_name": ["PSG", "OM"]}
    )
    id_en_nom(match_df, team_df)
    assert list(match_df.columns) == ["home_team", "away_team"]
    assert match_df["home_team"].tolist() == ["PSG", "OM"]
    assert match_df["away_team"].tolist() == ["OM", 3]


def test_get_saison():
    df = pd.DataFrame({"date": pd.to_datetime(["2020-09-15", "2021-05-10"])})
    result = get_saison(df)
    assert result["saison"].tolist() == ["2020/2021", "2020/2021"]


def test_creer_colonne_age_au_moment():
    df = pd.DataFrame(
        {
            "naissance": pd.to_datetime(["2000-01-01"]),
            "eval": pd.to_datetime(["2020-01-01"]),
        }
    )
    result = creer_colonne_age_au_moment(df, "naissance", "eval")
    assert result["age"].iloc[0] == 20


def test_creer_tranche_age():
    df = pd.DataFrame({"age": [20, 25, 30, 35, 40]})
    result = creer_tranche_age(df, "age")
    assert result["age_group"].tolist() == [
        "18-22",
        "23-27",
        "28-32",
        "33-37",
        "38+",
    ]


def test_filtrer_df_filtre_col_sans_valeur():
    df = pd.DataFrame({"A": [1, 2], "B": ["x", "y"]})
    # filtre_col est fourni mais filtre_val est None
    result = filtrer_df(df, filtre_col="A", filtre_val=None)
    pd.testing.assert_frame_equal(result, df)


@pytest.mark.parametrize(
    "nom, attendu",
    [
        ("Premier League (Angleterre)", 1729),
        ("Bundesliga (Allemagne)", 7809),
        ("Serie A (Italie)", 10257),
        ("Liga BBVA (Espagne)", 21518),
        ("Eredivisie (Pays-Bas)", 13274),
        ("Liga ZON Sagres (Portugal)", 17642),
        ("Ekstraklasa (Pologne)", 15722),
        ("Jupiler League (Belgique)", 1),
        ("Super League (Suisse)", 24558),
    ],
)
def test_id_championnat_complet(nom, attendu):
    assert id_championnat(nom) == attendu
