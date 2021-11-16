from dependency_injector import containers, providers

from inviter.io import SendInvite
from inviter.repository import PersonRepositoryJson

__all__ = ["Repositories", "IoAdapters"]


class Repositories(containers.DeclarativeContainer):
    Person = providers.Singleton(PersonRepositoryJson, "people.json")


class IoAdapters(containers.DeclarativeContainer):
    send_invite = providers.Singleton(SendInvite)
