from athletemgmt.model.app_configuration import AppConfiguration
from athletemgmt.model.athlete import Athlete
from athletemgmt.repository.athlete_repository import AthleteRepository


class AthleteService:
    def __init__(self, cfg: AppConfiguration):
        self.repository = AthleteRepository(cfg)

    def create_athlete(self, athlete: Athlete) -> Athlete:
        return self.repository.create(athlete)

    def get_athlete_by_id(self, athlete_id: int) -> Athlete:
        return self.repository.find_by_id(athlete_id)

    def list_athletes(self) -> list[Athlete]:
        return self.repository.find_all()

    def update_athlete(self, athlete: Athlete) -> Athlete:
        return self.repository.update(athlete.id, athlete.model_dump())

    def delete_athlete(self, athlete_id: int) -> None:
        self.repository.delete(athlete_id)
