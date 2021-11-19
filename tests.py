from datetime import datetime
from collections import namedtuple

import pytest

from command_bus import CommandHandlerNotFound
from bootstrap import bootstrap
from inviter.usecase import InviteAdultsToBar
from main import CliApp
from webapi import app as webapp


def test_bootstrap_invite_adults_to_bar():
    command_bus = bootstrap()
    command = InviteAdultsToBar(invitation_date=datetime(1978, 9, 15, 5, 10))
    send_invites_result = command_bus.handle(command)
    assert len(send_invites_result) > 0


def test_not_registered_command():
    command_bus = bootstrap()
    FakeCommand = namedtuple("command", [])
    command = FakeCommand()
    with pytest.raises(CommandHandlerNotFound):
        command_bus.handle(command)


def test_register_command():
    command_bus = bootstrap()
    FakeCommand = namedtuple("command", [])
    command = FakeCommand()
    command_bus.add_handler(FakeCommand, lambda x: 1)
    result = command_bus.handle(command)
    assert result == 1


def test_cli_app():
    result = CliApp().onecmd("invite_adults 2021-12-22 09:12")
    assert result == True


def test_cli_app_wrong_date():
    result = CliApp().onecmd("invite_adults 2021-13")
    assert result == False


@pytest.fixture
def web_client():
    with webapp.test_client() as client:
        yield client


def test_webapi(web_client):
    response = web_client.post("/invite/adults", json={"date": "1978-09-15", "hour": 5, "minute": 0})
    assert response.status_code == 200
    data = response.json
    assert "success" in data
    assert "failed" in data

def test_webapi_wrong_input(web_client):
    response = web_client.post("/invite/adults", json={})
    assert response.status_code == 400
    data = response.json
    assert "message" in data
