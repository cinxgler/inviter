import cmd
from datetime import datetime

from returns.pipeline import is_successful
from returns.result import safe
from toolz.itertoolz import groupby

import webapi
from bootstrap import bootstrap
from inviter.usecase import InviteAdultsToBar

DATE_FORMAT = "%Y-%m-%d %H:%M"

# Input Validator
@safe
def parse_time(time_to_validate: str) -> datetime:
    return datetime.strptime(time_to_validate, DATE_FORMAT)


# App
class CliApp(cmd.Cmd):
    """Invitations Management App"""

    def do_webserver(self, debug):
        """Runs a webserver"""
        webapi.app.run(debug=debug)

    def do_EOF(self, line):
        """Use CRTL+d to exit"""
        return True

    def do_invite_adults(self, invite_datetime):
        """invite_adults [invite_datetime]

        Send an invite to adults only to come at [invite_datetime]

        invite_date: on format "YYYY-MM-DD HH:MM"
        """
        invitation_date = parse_time(invite_datetime)
        if not is_successful(invitation_date):
            print(invitation_date.failure())
            return False

        command_bus = bootstrap()
        command = InviteAdultsToBar(invitation_date=invitation_date.unwrap())
        send_invites_result = command_bus.handle(command)

        result_by_success = groupby(is_successful, send_invites_result)
        for is_success, results in result_by_success.items():
            count = len(results)
            if is_success:
                msg = f"Success Count: {count}"
            else:
                msg = f"Failed Count: {count}"
            print(msg)
        return True


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        CliApp().onecmd(" ".join(sys.argv[1:]))
    else:
        CliApp().cmdloop()
