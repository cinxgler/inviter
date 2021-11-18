from datetime import date, datetime

from dependency_injector.wiring import Provide
from flask import Flask
from flask_restx import Api, Resource, fields
from pydantic import BaseModel, validator
from returns.pipeline import is_successful
from toolz.itertoolz import groupby

from bootstrap import bootstrap
from inviter.usecase import InviteAdultsToBar

app = Flask(__name__)
api = Api(app)

ns = api.namespace("invite", description="Send Invitations")

invitation_request = api.model(
    "InvitationRequest",
    {
        "date": fields.Date(required=True, description="Invitation date in ISO format yyyy-mm-dd"),
        "hour": fields.Integer(required=True, description="Hour"),
        "minute": fields.Integer(required=True, description="Minute"),
    },
)

invitation_response = api.model(
    "InvitationResponse",
    {
        "success": fields.Integer(required=True, description="Total count of invitations sent successfully"),
        "failed": fields.Integer(
            required=True,
            description="Total count of invitations that failed and weren't sent",
        ),
    },
)


class InvitationRequest(BaseModel):
    date: date
    hour: int
    minute: int

    @validator("hour")
    def less_than_24(cls, value):
        if 0 < value >= 24:
            raise ValueError("Values between 0 and 23 are valid")
        return value

    @validator("minute")
    def less_than_60(cls, value):
        if 0 < value >= 60:
            raise ValueError("Values between 0 and 59 are valid")
        return value


@ns.route("/adults")
class InviteAdults(Resource):
    @ns.doc("Send invitation to adults from the repository")
    @ns.expect(invitation_request)
    @ns.marshal_with(invitation_response, code=200)
    def post(self):
        invitation_request = InvitationRequest(**api.payload)
        raw_invitation_datetime = f"{invitation_request.date} {invitation_request.hour}:{invitation_request.minute}"
        invitation_date = datetime.strptime(raw_invitation_datetime, "%Y-%m-%d %H:%M")
        command_bus = bootstrap()
        command = InviteAdultsToBar(invitation_date=invitation_date)
        send_invites_result = command_bus.handle(command)

        result = {"success": 0, "failed": 0}
        result_by_success = groupby(is_successful, send_invites_result)
        for is_success, results in result_by_success.items():
            cnt = len([r for r in results])
            if is_success:
                result["success"] = cnt
            else:
                result["failed"] = cnt
        return result
