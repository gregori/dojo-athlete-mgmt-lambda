from athletemgmt.model.event import Event


def lambda_handler(event, _):
    event_obj = Event.model_validate(event)

    return {
        "statusCode": 200,
        "body": event_obj.model_dump()
    }
