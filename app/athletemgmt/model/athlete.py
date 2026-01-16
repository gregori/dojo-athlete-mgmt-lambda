from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class Athlete(BaseModel):
    id: str = Field(default="", description="UUID único do atleta (gerado automaticamente)")
    name: str = Field(..., description="Nome completo do atleta")
    cpf: str = Field(..., description="CPF do atleta")
    rg: str = Field(..., description="RG do atleta")
    email: Optional[str] = Field(..., description="Email do atleta")
    date_of_birth: date = Field(
        ...,
        description="Data de nascimento do atleta",
    )
    street: str = Field(..., description="Rua do atleta")
    number: int = Field(..., description="Número da casa do atleta")
    complement: Optional[str] = Field(
        ...,
        description="Complemento do endereço",
    )
    neighborhood: str = Field(..., description="Bairro do atleta")
    city: str = Field(..., description="Cidade do atleta")
    state: str = Field(..., description="Estado do atleta")
    zip_code: str = Field(..., description="CEP do atleta")
    phone: Optional[str] = Field(..., description="Telefone de contato")
    cellphone: Optional[str] = Field(..., description="Celular de contato")
    father_name: Optional[str] = Field(
        ...,
        description="Nome do pai do atleta",
    )
    mother_name: Optional[str] = Field(
        ...,
        description="Nome da mãe do atleta",
    )
    guardians_cpf: Optional[str] = Field(
        ...,
        description="CPF do responsável legal",
    )
    guardians_rg: Optional[str] = Field(
        ...,
        description="RG do responsável legal",
    )
    subscription_date: date = Field(
        ...,
        description="Data de inscrição do atleta",
    )
    anaj_date: date = Field(
        ...,
        description="Data de inscrição do atleta na ANAJ",
    )
    blood_type: Optional[str] = Field(
        ...,
        description="Tipo sanguíneo do atleta",
    )
    last_medical_exam: date = Field(
        ..., description="Data do último exame médico do atleta"
    )
    current_belt_id: int = Field(
        ...,
        description="ID do atual faixa do atleta",
    )
