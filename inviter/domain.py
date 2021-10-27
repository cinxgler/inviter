from enum import Enum, auto, unique

import attr
from attr import dataclass
from returns.curry import partial
from returns.functions import tap
from returns.io import IOResult, impure, impure_safe
from returns.pipeline import flow, is_successful
from returns.pointfree import bind, map_
from returns.result import Failure, Result, ResultE, Success, safe
from returns.unsafe import unsafe_perform_io
from typing_extensions import final

from inviter.exceptions import InvariantError

_AGE_MAX_LIMIT = 200
_ADULT_AGE_LOWER_LIMIT = 18


@unique
class ErrorCodes(Enum):
    INVALID_AGE = auto()
    ADULT_CANNOT_BE_UNDERAGE = auto()


class AgeUnits(Enum):  # YAGNI
    YEAR = "year"
    MONTH = "month"


@dataclass(frozen=True)
class PersonAge:
    age: int = attr.ib()
    unit: AgeUnits = AgeUnits.YEAR

    @age.validator
    def check_age_range(self, attribute, value):
        if value < 0 or value > _AGE_MAX_LIMIT:
            raise InvariantError(
                ErrorCodes.INVALID_AGE,
                f"{value} is not a valid person age.",
            )


@dataclass(frozen=True)
class Person:
    name: str
    age: PersonAge


@final
@dataclass(frozen=True)
class Adult(Person):
    age: PersonAge = attr.ib()

    @age.validator
    def check_age(self, attribute, value):
        if value.age < _ADULT_AGE_LOWER_LIMIT:
            raise InvariantError(
                ErrorCodes.ADULT_CANNOT_BE_UNDERAGE,
                f"{value.age} must be greater than {_ADULT_AGE_LOWER_LIMIT}",
            )


@final
@dataclass(frozen=True)
class Kid(Person):
    pass


def build_person(name: str, age: int) -> Person:
    if age >= _ADULT_AGE_LOWER_LIMIT:
        return Adult(
            name=name,
            age=PersonAge(age=age),
        )

    return Kid(
        name=name,
        age=PersonAge(age=age),
    )
