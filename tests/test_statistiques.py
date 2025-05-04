import pytest
import pandas as pd
from project.src.fonctions.statistiques import (
    calculer_moyenne,
    resume_colonne,
    nb_occurences,
    max_serie,
    compter_buts_matchs,
    saison_equipe,
    compter_actions_par_joueur,
    get_scorers_by_subtype,
    trier_joueurs_par_actions,
    nettoyer_attributs_techniques,
    calculer_ecart_type_technique_par_joueur,
    moyenne_ecart_type_par_joueur,
)


@pytest.fixture
def df_test():
    data = {
        "team": ["A", "B", "A", "B"],
        "team2": ["B", "A", "B", "A"],
        "goals": [1, 2, 3, 4],
        "goals2": [0, 2, 1, 1],
        "player": ["John", "Alice", "Bob", "Charlie"],
    }
    return pd.DataFrame(data)


def test_calculer_moyenne():
    # Test sur une liste
    assert calculer_moyenne([1, 2, 3]) == 2.0
    assert calculer_moyenne([5, 10]) == 7.5

    # Test sur un DataFrame
    df = pd.DataFrame({"team": ["A", "B", "A", "B"], "goals": [1, 2, 3, 4]})
    result = calculer_moyenne(df, group_by_col="team", value_col="goals")
    assert result == {"A": 2.0, "B": 3.0}


def test_resume_colonne(df_test):
    # Test max
    assert resume_colonne(df_test, "goals", operation="max") == 4
    # Test min
    assert (
        resume_colonne(df_test, "goals", col_b="player", operation="min") == 1
    )
    # Test diff_abs
    diff = resume_colonne(
        df_test, "goals", col_b="goals2", operation="diff_abs"
    )
    assert diff.equals(pd.Series([1, 0, 2, 3], name="goals"))


def test_nb_occurences(df_test):
    result = nb_occurences(df_test, "team")
    assert result["A"] == 2
    assert result["B"] == 2


def test_max_serie(df_test):
    idx, max_vals = max_serie(df_test[["goals"]])
    assert idx["goals"] == 3
    assert max_vals["goals"] == 4


def test_compter_buts_matchs():
    dic = {1: [2021, "league", 1, 2, 2, 3], 2: [2021, "league", 2, 1, 1, 1]}
    goals = {}
    result = compter_buts_matchs(dic, goals, 2, 4)
    assert result[1] == [2, 1]  # Team 1
    assert result[2] == [1, 1]  # Team 2


def test_saison_equipe():
    matchs = {1: [2021, "league", 1, 2, 2, 3], 2: [2021, "league", 2, 1, 1, 1]}
    result = saison_equipe(matchs)
    assert result[1][0] == 1  # Points of team 1
    assert result[2][0] == 4  # Points of team 2


def test_compter_actions_par_joueur():
    goal_dfs = [
        pd.DataFrame(
            {"player1": [1, 2, 3], "subtype": ["header", "volley", "header"]}
        ),
        pd.DataFrame({"player1": [1, 2], "subtype": ["header", "volley"]}),
    ]
    result = compter_actions_par_joueur(goal_dfs, "player1")
    assert result[1] == 2
    assert result[2] == 2
    assert result[3] == 1


def test_get_scorers_by_subtype():
    goal_dfs = [
        pd.DataFrame(
            {"player1": [1, 2, 3], "subtype": ["header", "volley", "header"]}
        ),
        pd.DataFrame({"player1": [1, 2], "subtype": ["header", "volley"]}),
    ]
    result = get_scorers_by_subtype(goal_dfs, "header")
    assert 1 in result
    assert 3 in result


def test_trier_joueurs_par_actions(df_test):
    compteur = {1: 10, 2: 5, 3: 7}
    player_df = pd.DataFrame(
        {"player_api_id": [1, 2, 3], "player_name": ["John", "Alice", "Bob"]}
    )
    result = trier_joueurs_par_actions(compteur, player_df, "buts", top_n=2)
    assert result.shape[0] == 2
    assert result["Joueur"].iloc[0] == "John"
    assert result["Joueur"].iloc[1] == "Bob"


def test_nettoyer_attributs_techniques():
    df = pd.DataFrame({"attr1": [1, 2, None, 4], "attr2": [None, 3, 4, 5]})
    result = nettoyer_attributs_techniques(df, ["attr1", "attr2"])
    assert result.shape[0] == 2  # Two rows should remain


def test_calculer_ecart_type_technique_par_joueur():
    df = pd.DataFrame({"attr1": [1, 2, 3], "attr2": [2, 3, 4]})
    result = calculer_ecart_type_technique_par_joueur(df, ["attr1", "attr2"])
    assert result["tech_std"].iloc[0] == 0.7071067811865476


def test_moyenne_ecart_type_par_joueur():
    df = pd.DataFrame(
        {"player_api_id": [1, 2, 1], "tech_std": [0.7, 0.6, 0.8]}
    )
    result = moyenne_ecart_type_par_joueur(df)
    assert result["tech_std"].iloc[0] == 0.75  # Average for player 1
