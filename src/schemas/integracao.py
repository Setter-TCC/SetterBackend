from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel, validator

from src.utils.enums import TipoPessoa


class IntegracaoIntegraSchema(BaseModel):
    id: Optional[UUID]
    data_inicio: datetime
    data_fim: Optional[Union[datetime, None]]
    ativo: Optional[bool]
    tipo_pessoa: int
    time_id: UUID
    pessoa_id: UUID

    @validator("tipo_pessoa")
    def validate_posicao(cls, tipo_pessoa):
        try:
            _ = TipoPessoa(value=tipo_pessoa)
            return tipo_pessoa
        except ValueError:
            raise ValueError("Erro ao receber o tipo de pessoa. "
                             "Os valores aceitos são:  "
                             "1-administrador   "
                             "2-atleta   "
                             "3-tecnico   ")

    class Config:
        orm_mode = True
