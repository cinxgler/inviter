import pytest

from inviter.domain import (
    Adult,
    Kid,
    build_person,
    _ADULT_AGE_LOWER_LIMIT,
    _AGE_MAX_LIMIT,
)
from inviter.exceptions import InvariantError


@pytest.mark.parametrize(
    "name,age,expected",
    [
        ("adult", 50, Adult),
        ("very old adult", _AGE_MAX_LIMIT, Adult),
        ("kid", 1, Kid),
        ("Adult", _ADULT_AGE_LOWER_LIMIT, Adult),
        ("kid", _ADULT_AGE_LOWER_LIMIT - 1, Kid),
    ],
)
def test_build_a_person(name, age, expected):
    person = build_person(name=name, age=age)
    assert isinstance(person, expected)


@pytest.mark.parametrize(
    "name,age",
    [
        ("too old", 10000),
        ("negative age", -1),
        ("just too old", _AGE_MAX_LIMIT + 1),
    ],
)
def test_cannot_build(name, age):
    with pytest.raises(InvariantError):
        build_person(name=name, age=age)
