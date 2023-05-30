from typing import Optional

from pydantic import BaseModel

from src.schemas.administrador import AdministradorSchema
from src.schemas.tecnico import TreinadorSchema
from src.schemas.time import TimeSchema


class ContaRequest(BaseModel):
    administrador: AdministradorSchema
    time: TimeSchema
    treinador: Optional[TreinadorSchema]

    class Config:
        orm_mode = True
