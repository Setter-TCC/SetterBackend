from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union


class Pessoa(BaseModel):
    id: int
    nome: str
    email: str
    cpf: str
    rg: str
    data_nascimento: datetime
    ddd: Union[str, None] = None
    numero: Union[str, None] = None

    class Config:
        orm_mode = True


class PessoaRequest(BaseModel):
    parameter: Pessoa = Field(...)

class Administrador(BaseModel):
    id: int
    nome_usuario: str
    senha: str

    class Config:
        orm_mode = True


class Atleta(BaseModel):
    id: int

    class Config:
        orm_mode = True


class Treinador(BaseModel):
    id: int
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
