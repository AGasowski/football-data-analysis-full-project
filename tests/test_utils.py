import pandas as pd
from src.fonctions.utils import (
    trier,
    formation,
    get_taille_joueurs,
    filtre_cartons,
    choix_criteres,
    nom_prenom,
    list_en_df,
    filtrer_par_pied,
    calcul_scores_postes,
    trouver_joueur_poste,
)


def test_trier_liste():
    data = [(1, "b"), (2, "a")]
    trier(data, par=1, type_data="liste", reverse=False)
    assert data == [(2, "a"), (1, "b")]


def test_trier_dataframe():
    df = pd.DataFrame({"A": [3, 1, 2]})
    result = trier(df, par="A", type_data="dataframe", reverse=False)
    assert result["A"].tolist() == [1, 2, 3]


def test_formation():
    abscisses = [2, 2, 2, 2, 4, 4, 6, 6, 6, 8, 10]
    assert formation(abscisses) == [4, 2, 3, 1, 1]


def test_get_taille_joueurs():
    df = pd.DataFrame({"player_api_id": [1], "height": [180]})
    assert get_taille_joueurs(df, 1) == 180
    assert get_taille_joueurs(df, 2) is None


def test_filtre_cartons():
    df1 = pd.DataFrame({"card_type": ["red", "yellow", "red"]})
    card = [df1]
    result = filtre_cartons(card, "red")
    assert len(result) == 1
    assert all(result[0]["card_type"] == "red")


def test_choix_criteres():
    criteres = choix_criteres()
    assert "GK" in criteres
    assert isinstance(criteres["GK"], list)
    assert "gk_reflexes" in criteres["GK"]


def test_nom_prenom():
    df = pd.DataFrame({"player_name": ["Cristiano Ronaldo", "Pelé"]})
    result = nom_prenom(df)
    assert result.loc[0, "prenom"] == "Cristiano"
    assert result.loc[0, "nom"] == "Ronaldo"
    assert result.loc[1, "prenom"] == ""
    assert result.loc[1, "nom"] == "Pelé"


def test_list_en_df():
    d = {"a": 1, "b": 2}
    df = list_en_df(d, "clé", "valeur")
    assert df.columns.tolist() == ["clé", "valeur"]
    assert df.shape == (2, 2)


def test_filtrer_par_pied():
    df = pd.DataFrame(
        {
            "preferred_foot": ["Right", "Left", "Right"],
            "player_api_id": [1, 2, 3],
        }
    )
    result = filtrer_par_pied(df, "DD")
    assert all(result["preferred_foot"].str.lower() == "right")


def test_calcul_scores_postes():
    df = pd.DataFrame(
        {
            "player_api_id": [1, 2],
            "gk_diving": [10, 5],
            "gk_handling": [10, 5],
            "gk_kicking": [10, 5],
            "gk_positioning": [10, 5],
            "gk_reflexes": [10, 5],
        }
    )
    dic = {
        "GK": [
            "gk_diving",
            "gk_handling",
            "gk_kicking",
            "gk_positioning",
            "gk_reflexes",
        ]
    }
    result = calcul_scores_postes(df, dic)
    assert "GK_score" in result.columns
    assert result["GK_score"].tolist() == [50, 25]


def test_trouver_joueur_poste():
    df = pd.DataFrame(
        {
            "player_api_id": [1, 2, 3],
            "AD_score": [90, 80, 70],
            "preferred_foot": ["Right", "Left", "Right"],
        }
    )
    joueurs_selectionnes = set([1])
    joueur = trouver_joueur_poste(df, "AD", joueurs_selectionnes)
    assert joueur == 3
