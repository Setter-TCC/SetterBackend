from datetime import datetime
from typing import Optional
from uuid import uuid4

import pytz

from src.schemas import PessoaSchema, IntegracaoIntegraSchema, ContaRequest, \
    AdministradorSchema, TimeSchema, TreinadorSchema
from src.utils.crypt import crypt_context
from src.utils.enums import TipoPessoa


def generate_payload_for_account_create(request: ContaRequest) -> (bool, bool, TimeSchema, PessoaSchema,
                                                                   AdministradorSchema, IntegracaoIntegraSchema,
                                                                   Optional[TreinadorSchema], Optional[PessoaSchema],
                                                                   Optional[IntegracaoIntegraSchema]):
    coach_sent: bool = request.treinador is not None
    coach_is_admin = request.administrador.email == request.treinador.email if coach_sent else False

    # ID's normalization
    request.administrador.id = uuid4()
    request.time.id = uuid4()
    if coach_sent:
        if coach_is_admin:
            request.treinador.id = request.administrador.id
        else:
            request.treinador.id = uuid4()

    # Team
    team = request.time

    # Admin manipulation
    admin_person = PessoaSchema(id=request.administrador.id, nome=request.administrador.nome,
                                email=request.administrador.email, cpf=request.administrador.cpf,
                                rg=request.administrador.rg, data_nascimento=request.administrador.data_nascimento,
                                telefone=request.administrador.telefone)
    admin = request.administrador
    admin.senha = crypt_context.hash(admin.senha)
    admin_integration = IntegracaoIntegraSchema(id=uuid4(),
                                                data_inicio=datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
                                                data_fim=None, ativo=True, time_id=team.id,
                                                tipo_pessoa=TipoPessoa.administrador.value, pessoa_id=admin.id)

    # Coach
    coach = None
    coach_person = None
    coach_integration = None
    if coach_sent:
        coach = request.treinador
        coach_person = PessoaSchema(id=request.treinador.id, nome=request.treinador.nome,
                                    email=request.treinador.email, cpf=request.treinador.cpf,
                                    rg=request.treinador.rg, data_nascimento=request.treinador.data_nascimento,
                                    telefone=request.treinador.telefone)
        coach_integration = IntegracaoIntegraSchema(id=uuid4(),
                                                    data_inicio=datetime.now(tz=pytz.timezone('America/Sao_Paulo')),
                                                    data_fim=None, ativo=True, tipo_pessoa=TipoPessoa.tecnico.value,
                                                    time_id=team.id, pessoa_id=coach.id)

    return (coach_sent, coach_is_admin, team, admin_person, admin,
            admin_integration, coach, coach_person, coach_integration)
