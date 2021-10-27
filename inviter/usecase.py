from datetime import datetime
from typing import Callable, List, final

from attr import dataclass
from returns.curry import partial
from returns.functions import tap
from returns.io import IOResult, IOResultE
from returns.pipeline import flow
from returns.unsafe import unsafe_perform_io

from inviter.io import FailedInvite, Invite, send_invite
from inviter.domain import Adult, Person

__all__ = ["InviteAdultsToBar"]


@dataclass(frozen=True)
class BarInvite(Invite):
    identifier: str
    person: Adult
    message: str


def build_bar_invite(invitation_datetime: datetime, person: Adult) -> BarInvite:
    msg = f"""Hi {person.name},

        you are a {person.age} years old adult.

        Please come to our bar at {invitation_datetime}
    """
    return BarInvite(person=person, message=msg, identifier=person.name)


@final
@dataclass(frozen=True)
class InviteAdultsToBar:
    _fetch_people: Callable[[], IOResultE[List[Person]]]
    _send_invite: Callable[[Invite], IOResult[Invite, FailedInvite]]

    def __call__(
        self, invitation_date: datetime
    ) -> List[IOResult[Invite, FailedInvite]]:
        build_bar_invite_ = partial(build_bar_invite, invitation_date)
        is_adult = lambda x: isinstance(x, Adult)

        people = self._fetch_people()

        send_invites = flow(
            people.value_or([]),
            #tap(print),
            unsafe_perform_io,
            partial(filter, is_adult),
            partial(map, build_bar_invite_),
            partial(map, self._send_invite),
        )

        return list([r for r in send_invites])
