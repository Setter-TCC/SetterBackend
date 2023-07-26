from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from pydantic import validator

from src.schemas.presenca import PresencaRequest
from src.utils.enums import TipoEvento


class EventoSchema(BaseModel):
    id: Optional[UUID]
    tipo_evento: int
    data: datetime
    local: Optional[str] = None
    nome: Optional[str] = None
    adversario: Optional[str] = None
    campeonato: Optional[str] = None
    observacao: Optional[str] = None
    time_id: UUID

    @validator("tipo_evento")
    def validate_posicao(cls, posicao):
        try:
            _ = TipoEvento(value=posicao)
            return posicao
        except ValueError:
            raise ValueError("Erro ao receber posição da atleta. "
                             "Os valores aceitos são:  "
                             "1-jogo   "
                             "2-treino   "
                             "3-evento")

    class Config:
        orm_mode = True


class EventoRequest(EventoSchema):
    lista_de_presenca: List[PresencaRequest]
