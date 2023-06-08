from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator, EmailStr

from src.utils.enums import NaipeTime


class TimeSchema(BaseModel):
    id: Optional[UUID]
    nome: str
    naipe: int
    cnpj: Optional[str]
    email: EmailStr

    class Config:
        orm_mode = True

    @validator("naipe")
    def validate_naipe(cls, naipe):
        try:
            _ = NaipeTime(value=naipe)
            return naipe

        except ValueError:
            raise ValueError("Erro ao receber o naipe do time.  "
                             "Os valores aceitos são: "
                             "1-feminino   "
                             "2-masculino   "
                             "3-misto")


class TimeRequest(BaseModel):
    id: UUID

    class Config:
        orm_mode = True
