from datetime import datetime

import pytest
from returns.io import IOFailure, IOResult, IOSuccess, impure_safe
from returns.pipeline import is_successful

from inviter.domain import build_person
from inviter.io import FailedInvite, Invite, SendInviteErrorCodes
from inviter.repository import PersonRepository
from inviter.usecase import InviteAdultsToBar, InviteAdultsToBarHandler


class TestPersonRepository(PersonRepository):
    @impure_safe
    def fetch_all_adults(self):
        return [
            build_person(name="John Doe", age=20),
            build_person(name="Foo Doe", age=20),
        ]

    @impure_safe
    def fetch_all_kids(self):
        return [
            build_person(name="Jr John Doe", age=2),
            build_person(name="Jr Foo Doe", age=5),
        ]

    @impure_safe
    def fetch_all_mix_adults_and_kids(self):
        return [
            build_person(name="John Doe", age=20),
            build_person(name="Jr John Doe", age=2),
            build_person(name="Jr Foo Doe", age=5),
            build_person(name="Foo Doe", age=20),
        ]


person_repository = TestPersonRepository()


def send_invite_ok(invite: Invite) -> IOResult[Invite, FailedInvite]:
    return IOSuccess(invite)


def send_invite_with_error(invite: Invite) -> IOResult[Invite, FailedInvite]:
    return IOFailure(FailedInvite(invite, SendInviteErrorCodes.CONNECTION_TIMEOUT))


@pytest.mark.parametrize(
    "repository_method,send_invite_function,expected_ok_count,expected_to_fail_count",
    [
        (person_repository.fetch_all_adults, send_invite_ok, 2, 0),
        (person_repository.fetch_all_kids, send_invite_ok, 0, 0),
        (person_repository.fetch_all_mix_adults_and_kids, send_invite_ok, 2, 0),
        #
        (person_repository.fetch_all_adults, send_invite_with_error, 0, 2),
        (person_repository.fetch_all_kids, send_invite_with_error, 0, 0),
        (person_repository.fetch_all_mix_adults_and_kids, send_invite_with_error, 0, 2),
    ],
)
def test_invite_adults_to_bar(repository_method, send_invite_function, expected_ok_count, expected_to_fail_count):
    invite_adults = InviteAdultsToBarHandler(fetch_people=repository_method, send_invite=send_invite_function)
    invite_command = InviteAdultsToBar(invitation_date=datetime(2021, 9, 15, 5, 45))
    send_invites_result = invite_adults(invite_command)
    ok_cnt = 0
    failed_cnt = 0
    for result in send_invites_result:
        if is_successful(result):
            ok_cnt += 1
        else:
            failed_cnt += 1
    assert ok_cnt == expected_ok_count
    assert failed_cnt == expected_to_fail_count
