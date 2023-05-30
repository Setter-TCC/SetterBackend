# Import de utilitários python
from datetime import datetime
from typing import Union
from uuid import uuid4

# Import do fastapi e sqlalchemy
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

import src.repositories.admin as admin_repository
import src.repositories.integracao as integracao_repository
# Import de repositories
import src.repositories.pessoa as pessoa_repository
import src.repositories.tecnico as tecnico_repository
import src.repositories.time as time_repository
# Import de configs
from src.configs.database import get_db
# Import de schemas
from src.schemas.conta import ContaRequest
from src.schemas.integracao import IntegracaoIntegraSchema
from src.schemas.pessoa import PessoaSchema
from src.schemas.tecnico import TreinadorSchema
# Import de utilitarios de codigo
from src.utils.crypt import crypt_context

account_router = APIRouter(prefix="/account")


@account_router.post("/", tags=["Conta"])
async def create_account(request: ContaRequest, db: Session = Depends(get_db)):
    request.administrador.id = uuid4()
    request.time.id = uuid4()
    if request.treinador:
        request.treinador.id = uuid4()

    # Definição de schemas do admin
    _pessoa_adm = PessoaSchema(id=request.administrador.id, nome=request.administrador.nome,
                               email=request.administrador.email, cpf=request.administrador.cpf,
                               rg=request.administrador.rg, data_nascimento=request.administrador.data_nascimento,
                               telefone=request.administrador.telefone)
    _administrador = request.administrador
    _administrador.senha = crypt_context.hash(_administrador.senha)

    # Definição de schemas do time
    _time = request.time

    # Definição de schemas do tecnico
    _pessoa_tecnico: Union[PessoaSchema, None] = None
    _tecnico: Union[TreinadorSchema, None] = None
    if request.treinador:
        _pessoa_tecnico = PessoaSchema(id=request.treinador.id, nome=request.treinador.nome,
                                       email=request.treinador.email, cpf=request.treinador.cpf,
                                       rg=request.treinador.rg, data_nascimento=request.treinador.data_nascimento,
                                       telefone=request.treinador.telefone)
        _tecnico = request.treinador

    _integracao_admin: Union[IntegracaoIntegraSchema, None] = None
    _integracao_tecnico: Union[IntegracaoIntegraSchema, None] = None

    # Cadastros de admin
    pessoa_repository.create_pessoa(db=db, pessoa=_pessoa_adm)
    admin_repository.create_admin(db=db, admin=_administrador)

    # Cadastros do time
    time_repository.create_time(db=db, time=_time)

    # Cadastro do técnico, se houver
    if _tecnico:
        pessoa_repository.create_pessoa(db=db, pessoa=_pessoa_tecnico)
        tecnico_repository.create_tecnico(db=db, tecnico=_tecnico)

    # TODO: Cadastro de integrações
    # Criação de integrações
    _integracao_admin = IntegracaoIntegraSchema(id=uuid4(), data_inicio=datetime.now(), data_fim=None, ativo=True,
                                                tipo_pessoa=1, time_id=_time.id, pessoa_id=_administrador.id)
    integracao_repository.create_integracao(db=db, integracao=_integracao_admin)

    if _tecnico:
        _integracao_tecnico = IntegracaoIntegraSchema(id=uuid4(), data_inicio=datetime.now(), data_fim=None, ativo=True,
                                                      tipo_pessoa=3, time_id=_time.id, pessoa_id=_tecnico.id)
        integracao_repository.create_integracao(db=db, integracao=_integracao_tecnico)

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "msg": "Sucesso"
        }
    )
