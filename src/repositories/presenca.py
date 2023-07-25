from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Presenca
from src.schemas import PresencaSchema


def create_presenca(db: Session, presenca: PresencaSchema):
    try:
        _presenca = Presenca(
            id=presenca.id,
            falta=presenca.falta,
            justificado=presenca.justificado,
            justificativa=presenca.justificativa,
            evento_id=presenca.evento_id,
            pessoa_id=presenca.pessoa_id
        )
        db.add(_presenca)
        db.commit()
        db.refresh(_presenca)
        return True

    except Exception:
        return False


def get_presencas(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Presenca).offset(skip).limit(limit).all()
        return query

    except Exception:
        return False


def get_presenca_by_id(db: Session, presenca_id: UUID):
    try:
        query = db.query(Presenca).filter_by(id=presenca_id).first()
        return query

    except Exception:
        return False


def get_presencas_by_evento_id(db: Session, evento_id: UUID):
    try:
        query = db.query(Presenca).filter_by(evento_id=evento_id).all()
        return query

    except Exception:
        return False


def update_presenca(db: Session, presenca: PresencaSchema):
    try:
        query = db.query(Presenca).filter_by(id=presenca.id).update({
            "falta": presenca.falta,
            "justificado": presenca.justificado,
            "justificativa": presenca.justificativa
        })
        db.commit()
        return query

    except Exception:
        return False
