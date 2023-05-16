from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union, Optional


class Pessoa(BaseModel):
    id: Optional[int]
    nome: str
    email: str
    cpf: str
    rg: str
    data_nascimento: datetime
    ddd: Optional[str] = None
    numero: Optional[str] = None

    class Config:
        orm_mode = True


class PessoaRequest(BaseModel):
    parameter: Pessoa = Field(...)

class Administrador(BaseModel):
    id: Optional[int]
    nome_usuario: str
    senha: str

    class Config:
        orm_mode = True


class Atleta(BaseModel):
    id: Optional[int]

    class Config:
        orm_mode = True


class Treinador(BaseModel):
    id: Optional[int]
    cref: str

    class Config:
        orm_mode = True


class Equipe(BaseModel):
    id: int
    nome: str
    estado: str
    cidade: Union[str, None] = None
    cnpj: Union[str, None] = None

    class Config:
        orm_mode = True


class IntegracaoIntegra(BaseModel):
    data_inicio: datetime
    data_fim: Union[datetime, None] = None
    ativo: bool = True
    tipo_pessoa: str
    equipe_id: int
    pessoa_id: int

    class Config:
        orm_mode = True
