import cmd
from datetime import datetime

from returns.pipeline import is_successful
from returns.result import safe
from toolz.itertoolz import groupby

import webapi
from inviter.usecase import InviteAdultsToBar
from usecases import bootstrap_usecase

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

        command = InviteAdultsToBar(invitation_date=invitation_date.unwrap())
        command_handler = bootstrap_usecase(command)
        send_invites_result = command_handler(command)

        result_by_success = groupby(is_successful, send_invites_result)
        for is_success, results in result_by_success.items():
            count = len(results)
            if is_success:
                msg = f"Success Count: {count}"
            else:
                msg = f"Failed Count: {count}"
            print(msg)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        CliApp().onecmd(" ".join(sys.argv[1:]))
    else:
        CliApp().cmdloop()

# for invite_result in send_invites_result:
#     if not is_successful(invite_result):
#         error = unsafe_perform_io(invite_result.failure())
#         print(f"Could send invite '{error.invite.identifier}' due to '{error.error_code}'")
