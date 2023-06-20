from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from pydantic import BaseModel

from src.schemas.pessoa import PessoaSchema


class TreinadorSchema(PessoaSchema):
    cref: Optional[str]


class TreinadorRequest(TreinadorSchema):
    time_id: UUID
    data_inicio: datetime


class EditTreinadorRequest(TreinadorRequest):
    data_fim: Union[datetime, None]


class TecnicoActivationRequest(BaseModel):
    tecnico_id: UUID
    time_id: UUID
    data_fim: Optional[Union[datetime, None]]

    class Config:
        orm_mode = True
