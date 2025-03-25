from typing import List, Optional

from athletemgmt.model.app_configuration import AppConfiguration
from athletemgmt.model.athlete import Athlete
from athletemgmt.service.db_service import DbService


class AthleteRepository:
    def __init__(self, cfg: AppConfiguration):
        self._db = DbService(cfg)
        # self._create_table()

    def _create_table(self):
        """Cria a tabela de atletas no banco DuckDB."""
        self._db.execute_query(
            """
        CREATE TABLE IF NOT EXISTS athletes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            date_of_birth DATE NOT NULL
        )
        """
        )

    def create(self, athlete: Athlete) -> Athlete:
        """Insere um novo atleta no banco."""
        self._db.execute_query(
            """
        INSERT INTO athletes (id, name, address, phone, date_of_birth)
        VALUES (?, ?, ?, ?, ?)
        """,
            (
                athlete.id,
                athlete.name,
                athlete.address,
                athlete.phone,
                athlete.date_of_birth,
            ),
        )

        return athlete

    def find_by_id(self, athlete_id: int) -> Optional[Athlete]:
        """Busca um atleta pelo ID."""
        row = self._db.execute_query(
            "SELECT * FROM athletes WHERE id = ?",
            (athlete_id,),
        ).fetchone()

        if row:
            return Athlete.model_validate(
                dict(
                    zip(
                        ["id", "name", "address", "phone", "date_of_birth"],
                        row,
                    )
                )
            )
        return None

    def find_all(self) -> List[Athlete]:
        """Retorna todos os atletas cadastrados."""
        rows = self._db.execute_query("SELECT * FROM athletes").fetchall()
        return [
            Athlete.model_validate(
                dict(
                    zip(
                        ["id", "name", "address", "phone", "date_of_birth"],
                        row,
                    )
                )
            )
            for row in rows
        ]

    def update(self, athlete_id: int, updates: dict) -> Optional[Athlete]:
        """Atualiza um atleta pelo ID."""
        updates_sql = ", ".join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values()) + [athlete_id]

        self._db.execute_query(
            f"UPDATE athletes SET {updates_sql} WHERE id = ?",
            tuple(values),
        )

        return self.find_by_id(athlete_id)

    def delete(self, athlete_id: int) -> None:
        """Deleta um atleta pelo ID."""
        self._db.execute_query(
            "DELETE FROM athletes WHERE id = ?",
            (athlete_id,),
        )
