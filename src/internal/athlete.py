from datetime import datetime
from typing import Tuple
from uuid import uuid4

import pytz

from src.schemas import PessoaSchema, AtletaSchema, IntegracaoIntegraSchema, AtletaRequest
from src.utils.enums import TipoPessoa


def generate_payload_for_athlete_create(request: AtletaRequest) \
        -> Tuple[AtletaSchema, IntegracaoIntegraSchema, PessoaSchema]:
    request.id = uuid4()
    pessoa_atleta = PessoaSchema(
        id=request.id,
        nome=request.nome,
        email=request.email,
        cpf=request.cpf,
        rg=request.rg,
        data_nascimento=request.data_nascimento,
        telefone=request.telefone
    )
    atleta = AtletaSchema(
        id=request.id,
        posicao=request.posicao,
        nome=request.nome,
        email=request.email
    )
    integracao = IntegracaoIntegraSchema(
        id=uuid4(),
        data_inicio=datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
        ativo=True,
        tipo_pessoa=TipoPessoa.atleta.value,
        time_id=request.time_id,
        pessoa_id=pessoa_atleta.id
    )

    return atleta, integracao, pessoa_atleta
