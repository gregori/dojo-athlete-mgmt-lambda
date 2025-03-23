from athletemgmt.model.app_configuration import AppConfiguration
from athletemgmt.model.event import Event
from athletemgmt.model.response import Response
from athletemgmt.processor.atlhete_processor import (
    AthleteProcessor,
    AthleteNotFoundError,
)


def lambda_handler(event, _):
    try:
        event_obj = Event.model_validate(event)
        cfg = AppConfiguration()  # type: ignore
        processor = AthleteProcessor(cfg)
        response = processor.process(event_obj)
    except ValueError as err:
        response = Response(status_code=400, body=str(err))
    except AthleteNotFoundError as err:
        response = Response(status_code=404, body=str(err))

    return response.model_dump(by_alias=True, exclude_none=True)
