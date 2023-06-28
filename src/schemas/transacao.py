from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, validator

from src.utils.enums import TipoTransacao


class TransacaoSchema(BaseModel):
    id: Optional[Union[UUID, None]] = None
    nome: Optional[Union[str, None]] = None
    descricao: Optional[Union[str, None]] = None
    data_acontecimento: datetime
    tipo: int
    valor: float
    time_id: UUID
    pessoa_id: Optional[Union[UUID, None]] = None

    @validator("valor")
    def validate_valor(cls, valor):
        if valor == 0.0:
            raise ValueError("Uma transação não pode ter valor zero")

        return valor

    @validator("tipo")
    def validate_tipo(cls, tipo):
        try:
            _ = TipoTransacao(tipo)
            return tipo
        except ValueError:
            raise ValueError("Erro ao receber tipo de transação da atleta. "
                             "Os valores aceitos são:  "
                             "1-Mensalidade   "
                             "2-Pagamento de técnico   "
                             "3-Despesa   "
                             "4-Ganho   ")

    class Config:
        orm_mode = True
