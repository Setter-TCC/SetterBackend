from datetime import datetime
from typing import Optional
from uuid import UUID

from src.schemas.pessoa import PessoaSchema

from pydantic import BaseModel, EmailStr


class AdministradorSchema(PessoaSchema):
    nome_usuario: str
    senha: str


class AdministradorUpdate(BaseModel):
    id: Optional[UUID]
    nome: str
    email: EmailStr
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[datetime] = None
    telefone: Optional[str] = None
    nome_usuario: str
    senha: Optional[str] = None
    nova_senha: Optional[str] = None

    class Config:
        orm_mode = True

