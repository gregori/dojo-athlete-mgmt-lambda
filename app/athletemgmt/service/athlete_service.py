from dojocommons.model.app_configuration import AppConfiguration
from dojocommons.service.base_service import BaseService

from athletemgmt.model.athlete import Athlete
from athletemgmt.repository.athlete_repository import AthleteRepository


class AthleteService(BaseService[Athlete]):
    def __init__(self, cfg: AppConfiguration):
        super().__init__(cfg, AthleteRepository)
