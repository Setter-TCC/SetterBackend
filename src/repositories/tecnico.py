from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Treinador, Pessoa, IntegracaoIntegra
from src.schemas.tecnico import TreinadorSchema
from src.utils.enums import TipoPessoa


def create_tecnico(db: Session, tecnico: TreinadorSchema):
    try:
        _tecnico = Treinador(
            id=tecnico.id,
            cref=tecnico.cref
        )
        db.add(_tecnico)
        db.commit()
        db.refresh(_tecnico)

        return True

    except Exception:
        return False


def get_all_tecnicos(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Treinador).offset(skip).limit(limit).all()
        return query

    except Exception:
        return False


def get_coach_from_team(db: Session, time_id: UUID):
    try:
        query = db.query(Pessoa, Treinador, IntegracaoIntegra) \
            .join(Treinador, Pessoa.id == Treinador.id) \
            .join(IntegracaoIntegra, Pessoa.id == IntegracaoIntegra.pessoa_id) \
            .filter(
            IntegracaoIntegra.tipo_pessoa == TipoPessoa.tecnico,
            IntegracaoIntegra.time_id == time_id,
            IntegracaoIntegra.ativo == True
        ).all()
        return query

    except Exception:
        return False


def get_tecnico_by_id(db: Session, id_tecnico: UUID):
    try:
        query = db.query(Treinador).filter_by(id=id_tecnico).first()
        return query

    except Exception:
        return False


def update_tecnico(db: Session, tecnico: TreinadorSchema):
    try:
        query = db.query(Treinador).filter_by(id=tecnico.id).update({
            "cref": tecnico.cref
        })
        db.commit()
        return query

    except Exception:
        return False


def delete_tecnico(db: Session, id_tecnico: UUID):
    try:
        db.query(Treinador).filter_by(id=id_tecnico).delete()
        db.commit()
        return True

    except Exception:
        return False
