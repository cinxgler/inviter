"""This is in charge of wiring the Dependency Injection on Command Bus"""

from typing import Callable

import di_containers
from classes import typeclass
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from returns.io import IOResult

from inviter.io import FailedInvite, Invite
from inviter.repository import PersonRepository
from inviter.usecase import InviteAdultsToBar, InviteAdultsToBarHandler


@typeclass
def bootstrap_usecase(cmd) -> Callable:
    """Return the Use Case handler with the injected dependencies"""


@bootstrap_usecase.instance(InviteAdultsToBar)
def bootstrap_usecase_invite_adult_to_bar(
    cmd: InviteAdultsToBar,
) -> InviteAdultsToBarHandler:
    repo: PersonRepository = di_containers.Repositories().Person()
    send_invite: Callable[
        [Invite], IOResult[Invite, FailedInvite]
    ] = di_containers.IoAdapters().send_invite()

    return InviteAdultsToBarHandler(
        fetch_people=repo.fetch_people, send_invite=send_invite
    )
