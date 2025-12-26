from dojocommons.controller.base_controller import BaseController
from dojocommons.model.app_configuration import AppConfiguration
from athletemgmt.model.athlete import Athlete
from athletemgmt.model.resource import Resource
from athletemgmt.service.athlete_service import AthleteService


class AthleteController(BaseController[Athlete]):
    def __init__(self, cfg: AppConfiguration):
        super().__init__(cfg, AthleteService, Resource.ATHLETES.value, Athlete)
