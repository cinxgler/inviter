import random
from enum import Enum
from datetime import datetime
from typing import Callable, List, Union, final

from attr import dataclass
from returns.curry import partial
from returns.functions import tap
from returns.io import IOFailure, IOResult, IOSuccess


class SendInviteErrorCodes(Enum):
    CONNECTION_TIMEOUT = "connection timeout"
    BAD_REQUEST = "bad request"


@dataclass
class Invite:
    identifier: str
    message: str


@dataclass
class FailedInvite:
    invite: Invite
    error_code: SendInviteErrorCodes


def send_invite(invite: Invite) -> IOResult[Invite, FailedInvite]:
    if random.choice([0, 1]):
        return IOFailure(
            FailedInvite(
                invite=invite, error_code=SendInviteErrorCodes.CONNECTION_TIMEOUT
            )
        )
    print("Sending invite ...", invite.message)
    return IOSuccess(invite)
