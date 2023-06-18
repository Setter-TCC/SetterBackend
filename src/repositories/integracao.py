from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from src.models import IntegracaoIntegra
from src.schemas.integracao import IntegracaoIntegraSchema
from src.utils.enums import TipoPessoa


def create_integracao(db: Session, integracao: IntegracaoIntegraSchema):
    try:
        _integracao = IntegracaoIntegra(
            id=integracao.id,
            data_inicio=integracao.data_inicio,
            ativo=integracao.ativo,
            tipo_pessoa=TipoPessoa(integracao.tipo_pessoa),
            time_id=integracao.time_id,
            pessoa_id=integracao.pessoa_id
        )
        db.add(_integracao)
        db.commit()
        db.refresh(_integracao)
        return True

    except Exception:
        return False


def get_integracoes(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(IntegracaoIntegra).offset(skip).limit(limit).all()
        return query

    except Exception:
        return False


def get_integracao_by_id(db: Session, integracao_id: UUID):
    try:
        query = db.query(IntegracaoIntegra).filter(IntegracaoIntegra.id == integracao_id).first()
        return query

    except Exception:
        return False


def get_integracao_by_user_and_team_id(db: Session, user_id: UUID, team_id: UUID):
    try:
        query = db.query(IntegracaoIntegra) \
            .filter_by(time_id=team_id, pessoa_id=user_id) \
            .first()
        return query

    except Exception:
        return False


def get_integracoes_by_time_id(db: Session, time_id: UUID):
    try:
        query = db.query(IntegracaoIntegra).filter_by(time_id=time_id).all()
        return query

    except Exception:
        return False


def get_integracoes_by_pessoa_id(db: Session, pessoa_id: UUID):
    try:
        query = db.query(IntegracaoIntegra).filter_by(pessoa_id=pessoa_id).all()
        return query

    except Exception:
        return False


def get_admin_integracao_by_pessoa_id(db: Session, pessoa_id: UUID):
    try:
        query = db.query(IntegracaoIntegra).filter_by(pessoa_id=pessoa_id, tipo_pessoa=TipoPessoa.administrador).first()
        return query

    except Exception:
        return False


def update_integracao(db: Session, integracao: IntegracaoIntegraSchema):
    try:
        query = db.query(IntegracaoIntegra).filter_by(id=integracao.id).update({
            "data_inicio": integracao.data_inicio,
            "data_fim": integracao.data_fim,
            "ativo": integracao.ativo
        })
        db.commit()
        return query

    except Exception:
        return False


def update_integracao_active_state(db: Session, integration_id: UUID, active: bool):
    try:
        query = db.query(IntegracaoIntegra).filter_by(id=integration_id).update({"ativo": active})
        db.commit()
        return query

    except Exception:
        return False


def remove_from_team(db: Session, integration_id: UUID):
    try:
        query = db.query(IntegracaoIntegra).filter_by(id=integration_id).update({
            "ativo": False,
            "data_fim": datetime.now()
        })
        db.commit()
        return query

    except Exception:
        return False
