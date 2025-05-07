import pytest
import pandas as pd

from project.src.fonctions.data_loader import (
    charger_csv,
    transforme,
    data_to_dict,
    convertir_colonne,
    fusionner_colonnes_en_listes,
)


def test_charger_csv_dataframe(tmp_path):
    csv_content = "id,name\n1,Alice\n2,Bob"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    df = charger_csv(str(csv_file))
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert list(df.columns) == ["id", "name"]


def test_charger_csv_dict(tmp_path):
    csv_content = "id,name,age\n1,Alice,30\n2,Bob,25"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    result = charger_csv(str(csv_file), "dict", "id", "name", "age")
    assert result == {1: ("Alice", "30"), 2: ("Bob", "25")}


def test_charger_csv_invalid():
    with pytest.raises(ValueError):
        charger_csv("fake.csv", mode="dict")


def test_transforme():
    xml_data = """
    <root>
        <value>
            <name>John</name>
            <age>30</age>
            <stats>
                <height>180</height>
                <weight>75</weight>
            </stats>
        </value>
        <value>
            <name>Jane</name>
            <age>28</age>
            <stats>
                <height>165</height>
                <weight>60</weight>
            </stats>
        </value>
    </root>
    """
    df = transforme(xml_data)
    assert df.shape == (2, 4)
    assert list(df.columns) == ["name", "age", "stats_height", "stats_weight"]
    assert df.iloc[0]["name"] == "John"
    assert df.iloc[1]["stats_weight"] == "60"


def test_data_to_dict():
    df = pd.DataFrame({"A": ["x", "y"], "B": [1, 2]})
    result = data_to_dict(df, "A", "B")
    assert result == {"x": 1, "y": 2}


def test_convertir_colonne_list():
    df = pd.DataFrame({"col": [10, 20, 30]})
    result = convertir_colonne(df, "col", "list")
    assert result == [10, 20, 30]


def test_convertir_colonne_invalide():
    df = pd.DataFrame({"col": ["a", "b"]})
    with pytest.raises(ValueError):
        convertir_colonne(df, "col", "float")


def test_fusionner_colonnes_en_listes():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4], "C": [5, 6]})
    result = fusionner_colonnes_en_listes(df, ["A", "C"])
    assert result == [[1, 5], [2, 6]]


def test_fusionner_colonnes_en_listes_invalide():
    df = pd.DataFrame({"A": [1, 2]})
    with pytest.raises(ValueError):
        fusionner_colonnes_en_listes(df, ["A", "Z"])


def test_charger_csv_dict_sans_id(tmp_path):
    csv_content = "name,age\nAlice,30\nBob,25"
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(csv_content)

    with pytest.raises(KeyError):
        charger_csv(str(csv_file), "dict", "id", "name", "age")


def test_transforme_xml_vide():
    xml_data = """<root></root>"""
    df = transforme(xml_data)
    assert df.empty


def test_convertir_colonne_type_inconnu():
    df = pd.DataFrame({"col": ["a", "b"]})
    with pytest.raises(ValueError):
        convertir_colonne(df, "col", "unknown_type")


def test_fusionner_colonnes_en_listes_colonnes_vides():
    df = pd.DataFrame({"A": [], "B": []})
    result = fusionner_colonnes_en_listes(df, ["A", "B"])
    assert result == []
