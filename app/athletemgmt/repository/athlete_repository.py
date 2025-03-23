from sqlalchemy.orm import Session

from athletemgmt.model.athlete import Athlete


class AthleteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, athlete: Athlete):
        self.session.add(athlete)
        self.session.commit()
        return athlete

    def find_by_id(self, athlete_id: int):
        return (
            self.session.query(Athlete)
            .filter(Athlete.id == athlete_id)
            .first()
        )

    def find_all(self):
        return self.session.query(Athlete).all()

    def update(self, athlete: Athlete):
        self.session.add(athlete)
        self.session.commit()
        return athlete

    def delete(self, athlete_id: int):
        athlete = self.find_by_id(athlete_id)
        if athlete:
            self.session.delete(athlete)
            self.session.commit()
