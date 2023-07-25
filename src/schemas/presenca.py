from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PresencaSchema(BaseModel):
    id: Optional[UUID]
    falta: bool
    justificado: Optional[bool] = False
    justificativa: Optional[str] = None
    pessoa_id: UUID
    evento_id: UUID

    class Config:
        orm_mode = True
