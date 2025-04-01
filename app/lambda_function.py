from dojocommons.model.app_configuration import AppConfiguration

from athletemgmt.controller.athlete_controller import AthleteController
from athletemgmt.model.event import Event
from athletemgmt.model.response import Response


def lambda_handler(event, _):
    try:
        event_obj = Event.model_validate(event)
        cfg = AppConfiguration()  # type: ignore
        controller = AthleteController(cfg)
        response = controller.dispatch(event_obj)
    except ValueError as err:
        response = Response(status_code=400, body=str(err))

    return response.model_dump(by_alias=True, exclude_none=True)
