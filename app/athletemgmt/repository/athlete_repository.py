from dojocommons.model.app_configuration import AppConfiguration
from dojocommons.repository.base_repository import BaseRepository

from athletemgmt.model.athlete import Athlete


class AthleteRepository(BaseRepository[Athlete]):
    def __init__(self, cfg: AppConfiguration):
        super().__init__(cfg, Athlete, "athletes")
        self._db.create_table_from_parquet("athletes")