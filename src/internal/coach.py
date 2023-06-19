from typing import Tuple
from uuid import uuid4

from sqlalchemy.orm import Session

from src.repositories import integracao_repository
from src.schemas import PessoaSchema, IntegracaoIntegraSchema, TreinadorRequest, TreinadorSchema, EditTreinadorRequest
from src.utils.enums import TipoPessoa


def generate_payload_for_coach_create(request: TreinadorRequest) \
        -> Tuple[TreinadorSchema, IntegracaoIntegraSchema, PessoaSchema]:
    pessoa_tecnico = PessoaSchema(
        id=request.id,
        nome=request.nome,
        email=request.email,
        cpf=request.cpf,
        rg=request.rg,
        data_nascimento=request.data_nascimento,
        telefone=request.telefone
    )
    tecnico = TreinadorSchema(
        id=request.id,
        nome=request.nome,
        email=request.email,
        cpf=request.cpf,
        rg=request.rg,
        data_nascimento=request.data_nascimento,
        telefone=request.telefone,
        cref=request.cref
    )
    integracao = IntegracaoIntegraSchema(
        id=uuid4(),
        data_inicio=request.data_entrada,
        ativo=True,
        tipo_pessoa=TipoPessoa.tecnico.value,
        time_id=request.time_id,
        pessoa_id=pessoa_tecnico.id
    )

    return tecnico, integracao, pessoa_tecnico


def generate_payload_for_coach_update(db: Session, request: EditTreinadorRequest) \
        -> Tuple[TreinadorSchema, PessoaSchema, IntegracaoIntegraSchema]:
    pessoa_tecnico = PessoaSchema(
        id=request.id,
        nome=request.nome,
        email=request.email,
        cpf=request.cpf,
        rg=request.rg,
        data_nascimento=request.data_nascimento,
        telefone=request.telefone
    )
    tecnico = TreinadorSchema(
        id=request.id,
        nome=request.nome,
        email=request.email,
        cpf=request.cpf,
        rg=request.rg,
        data_nascimento=request.data_nascimento,
        telefone=request.telefone,
        cref=request.cref
    )
    _integracao = integracao_repository.get_tecnico_integracao_by_pessoa_id(db=db, pessoa_id=tecnico.id)
    integracao_tecnico = IntegracaoIntegraSchema(
        id=_integracao.id,
        data_inicio=request.data_entrada,
        data_fim=request.data_fim,
        ativo=False if request.data_fim is not None else True,
        tipo_pessoa=TipoPessoa.tecnico.value,
        time_id=request.time_id,
        pessoa_id=pessoa_tecnico.id
    )

    return tecnico, pessoa_tecnico, integracao_tecnico
