from typing import Optional
from uuid import UUID

from pydantic import BaseModel, validator

from src.utils.enums import EstadoAtletaEvento


class PresencaSchema(BaseModel):
    id: Optional[UUID]
    falta: bool
    justificado: Optional[bool] = False
    justificativa: Optional[str] = None
    pessoa_id: UUID
    evento_id: UUID

    class Config:
        orm_mode = True


class PresencaRequest(BaseModel):
    id_atleta: UUID
    nome: str
    estado: int
    justificativa: Optional[str]

    @validator("estado")
    def validate_posicao(cls, posicao):
        try:
            _ = EstadoAtletaEvento(value=posicao)
            return posicao
        except ValueError:
            raise ValueError("Erro ao receber posição da atleta. "
                             "Os valores aceitos são:  "
                             "1-presente   "
                             "2-falta   "
                             "3-justificado")

    class Config:
        orm_mode = True
