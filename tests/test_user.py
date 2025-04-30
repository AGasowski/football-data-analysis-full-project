from project.model.user import User
import pytest


def test_ismajeur():
    user = User(18)
    assert user.is_majeur() is True


@pytest.mark.parametrize(
    "age,expected",
    [
        (30, True),
        (10, False),
    ],
)
def test_ismajeurparametrize(age, expected):
    user = User(age)
    assert user.is_majeur() == expected
