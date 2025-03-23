from sqlalchemy import Column, Integer, String, Date

from athletemgmt.service.db_service import Base


class Athlete(Base):
    __tablename__ = "athletes"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Athlete(id={self.id}, name={self.name}, date_of_birth={self.date_of_birth})>"
