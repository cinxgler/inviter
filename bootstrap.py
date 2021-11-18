"""This is in charge of wiring the Dependency Injection on Command Bus"""

from typing import Callable, List

import di_containers
from classes import typeclass
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from pymessagebus import CommandBus  # type: ignore
from returns.io import IOResult

import command_bus as commandbus
from inviter.io import FailedInvite, Invite
from inviter.repository import PersonRepository
from inviter.usecase import InviteAdultsToBar, InviteAdultsToBarHandler


def bootstrap() -> CommandBus:
    return commandbus


@commandbus.register_handler(InviteAdultsToBar)
def execute_invite_adult_to_bar(
    cmd: InviteAdultsToBar,
) -> List[IOResult[Invite, FailedInvite]]:
    repo = di_containers.Repositories().Person()
    send_invite = di_containers.IoAdapters().send_invite()
    handler = InviteAdultsToBarHandler(fetch_people=repo.fetch_people, send_invite=send_invite)
    return handler(cmd)
