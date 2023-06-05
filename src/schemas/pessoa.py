from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr


class PessoaSchema(BaseModel):
    id: Optional[UUID]
    nome: str
    email: EmailStr
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    telefone: Optional[str] = None  # TODO: Fazer validação de tamanho

    class Config:
        orm_mode = True
