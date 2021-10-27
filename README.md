# Experimenting with Typed Functional Programming in Python

This is a toy app that uses [results library](https://github.com/dry-python/returns) to build a module that follows basic principles of Typed Functional Programming, inspired on the following articles and books
- [Python exceptions considered an anti-pattern](https://sobolevn.me/2019/02/python-exceptions-considered-an-antipattern)
- [Enforcing Single Responsibility Principle in Python](https://sobolevn.me/2019/03/enforcing-srp)
- [Domain Modeling Made Functional](https://pragprog.com/titles/swdddf/domain-modeling-made-functional/)

The module implements a simple app that sends an invitation to adults from a list of people (including underage). This have two user interfaces, command line and REST API.

## Modules

The `inviter` package has the following modules:

- inviter/domain.py: Contains the core types to model people for this app, it contains the invariants and factory functions that allow to build the required entities.
- inviter/exceptions.py: Include a simple `InvariantException` that is raised when a Invariant is broken in the domain. The exception requires a `ErrorCode` to state the type of error found.
- inviter/io.py: It contains the function sends an invite, the function is impure and can fail randomly.
- inviter/repository. It contains functions that retrieves people data from memory or a json file `people.json`, they return entities using the domain types.
- inviter/usecase.py: It contains the main use case that receives a DateTime value that stated when the invited person should attend to the event. It fetches the people, filter by adults, build the invitation and sends the invite. Dependencies to repository and IO are given as parameters.


## Run

- Create virtual environment and install dependencies

    virtualenv -p python3.8 venv
    source venv/bin/activate
    pip install -r requirements.txt

- Run command line interface

    python main.py invite_adults "1978-09-15 10:00"

- Run web api

    python main.py webserver

- You can run the test suite using and get the coverage HTML report `htmlcov` folder

    pytest

- You can check the typing using

    mypy
