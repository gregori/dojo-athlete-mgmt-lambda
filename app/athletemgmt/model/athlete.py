from datetime import date

from pydantic import BaseModel, Field


class Athlete(BaseModel):
    id: int = Field(..., description="Identificador único do atleta")
    name: str = Field(..., description="Nome completo do atleta")
    address: str = Field(..., description="Endereço do atleta")
    phone: str = Field(..., description="Telefone de contato")
    date_of_birth: date = Field(
        ..., description="Data de nascimento do atleta"
    )
