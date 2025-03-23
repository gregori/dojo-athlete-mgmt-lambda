import duckdb
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from athletemgmt.model.app_configuration import AppConfiguration

Base = declarative_base()


class DbService:
    def __init__(self, app_cfg: AppConfiguration):
        self._app_cfg = app_cfg
        self._init_duckdb()
        self._engine = self._create_engine()

    def _init_duckdb(self):
        duckdb.sql("INSTALL httpfs; LOAD httpfs;")
        duckdb.sql(f"SET s3_region='{self._app_cfg.aws_region}';")
        duckdb.sql(
            f"SET s3_access_key_id='{self._app_cfg.aws_access_key_id}';"
        )
        duckdb.sql(
            f"SET s3_secret_access_key="
            f"'{self._app_cfg.aws_secret_access_key}';"
        )

        duckdb.sql(
            f"CREATE TABLE athletes AS SELECT * "
            f"FROM read_csv_auto('{self._app_cfg.s3_file_path}');"
        )

    @staticmethod
    def _create_engine():
        engine = create_engine("duckdb:///athletemgmt.db")
        Base.metadata.create_all(engine)

        return engine

    @property
    def session(self):
        session = sessionmaker(bind=self._engine)
        return session()
