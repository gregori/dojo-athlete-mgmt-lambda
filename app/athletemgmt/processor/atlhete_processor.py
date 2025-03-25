import json
from http import HTTPMethod
from typing import Callable, Dict

from athletemgmt.model.app_configuration import AppConfiguration
from athletemgmt.model.athlete import Athlete
from athletemgmt.model.event import Event
from athletemgmt.model.resource import Resource
from athletemgmt.model.response import Response
from athletemgmt.repository.athlete_repository import AthleteRepository
from athletemgmt.service.athlete_service import AthleteService
from athletemgmt.service.db_service import DbService


class AthleteNotFoundError(Exception):
    pass


class AthleteProcessor:
    def __init__(self, cfg: AppConfiguration):
        self._cfg = cfg
        db_service = DbService(self._cfg)
        athlete_repository = AthleteRepository(db_service.session)
        self._athlete_service = AthleteService(athlete_repository)

        self._strategy: Dict[HTTPMethod, Callable[[Event], Response]] = {
            HTTPMethod.GET: self._get_athlete,
            HTTPMethod.POST: self._post_athlete,
            HTTPMethod.PUT: self._put_athlete,
            HTTPMethod.DELETE: self._delete_athlete,
        }

    def process(self, event: Event):
        method = self._strategy.get(event.http_method)
        return method(event)

    def _get_athlete(self, event: Event):
        if event.resource == Resource.ATHLETES:
            return self._list_athletes(event)
        elif event.resource == Resource.ATHLETES_ID:
            return self._get_athlete_by_id(event)

    def _list_athletes(self, event: Event):
        athletes = self._athlete_service.list_athletes()
        athlete_list = {"athletes": [athlete.json() for athlete in athletes]}
        return Response(
            status_code=200,
            body=json.dumps(athlete_list, ensure_ascii=False),
        )

    def _get_athlete_by_id(self, event: Event):
        athlete_id = event.path_parameters.id
        athlete = self._athlete_service.get_athlete_by_id(int(athlete_id))
        return Response(status_code=200, body=athlete.json(ensure_ascii=False))

    def _post_athlete(self, event: Event):
        athlete = Athlete.parse_raw(event.body)
        athlete = self._athlete_service.create_athlete(athlete)

        return Response(status_code=201, body=athlete.json(ensure_ascii=False))

    def _put_athlete(self, event: Event):
        athlete_id = event.path_parameters.get("id")
        athlete = self._athlete_service.get_athlete_by_id(int(athlete_id))

        if not athlete:
            raise AthleteNotFoundError(
                f"Atleta com id {athlete_id} não encontrado."
            )

        updates = Athlete.parse_raw(event.body)
        athlete = self._athlete_service.update_athlete(updates)

        return Response(status_code=200, body=athlete.json(ensure_ascii=False))

    def _delete_athlete(self, event: Event):
        athlete_id = event.path_parameters.get("id")

        self._athlete_service.delete_athlete(int(athlete_id))

        return Response(status_code=204, body=None)
