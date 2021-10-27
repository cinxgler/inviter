import random
import json
from typing import List

from returns.io import impure_safe

from inviter.domain import Person, build_person


class PersonRepository:
    @impure_safe
    def fetch_people(self) -> List[Person]:
        return [
            build_person(name="John Doe", age=random.randint(1, 17)),
            build_person(name="Foo Doe", age=random.randint(1, 100)),
            build_person(name="Sr Foo Doe", age=random.randint(18, 100)),
            build_person(name="Sr Mary Doe", age=random.randint(18, 100)),
        ]


class PersonRepositoryJson(PersonRepository):
    def __init__(self, filename) -> None:
        self.filename = filename

    @impure_safe
    def fetch_people(self) -> List[Person]:
        result = []
        with open(self.filename) as json_file:
            json_data = json.load(json_file)
            for record in json_data:
                result.append(
                    build_person(
                        name=record["name"],
                        age=record["age"],
                    )
                )
        return result
