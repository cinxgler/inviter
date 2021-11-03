from dependency_injector import containers, providers

from inviter.io import SendInvite
from inviter.repository import PersonRepositoryJson, PersonRepository


class Repositories(containers.DeclarativeContainer):
    Person = providers.Singleton(PersonRepositoryJson, "people.json")

class TestRepositories(containers.DeclarativeContainer):
    Person = providers.Singleton(PersonRepository)

class IoAdapters(containers.DeclarativeContainer):
    send_invite = providers.Singleton(SendInvite)

class TestIoAdapters(containers.DeclarativeContainer):
    send_invite = providers.Singleton(SendInvite)
