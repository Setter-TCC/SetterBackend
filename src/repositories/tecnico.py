from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Treinador
from src.schemas.tecnico import TreinadorSchema


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
        db.rollback()
        return False


def get_all_tecnicos(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Treinador).offset(skip).limit(limit).all()
        return query

    except Exception:
        db.rollback()
        return False


def get_tecnico_by_id(db: Session, id_tecnico: UUID):
    try:
        query = db.query(Treinador).filter(Treinador.id == id_tecnico).first()
        return query

    except Exception:
        db.rollback()
        return False


def update_tecnico(db: Session, id_tecnico: UUID):
    try:
        query = db.query(Treinador).filter(Treinador.id == id_tecnico).first()
        # atualizar para cada campo enviado
        db.commit()
        return query

    except Exception:
        db.rollback()
        return False


def delete_tecnico(db: Session, id_tecnico: UUID):
    try:
        db.query(Treinador).filter(Treinador.id == id_tecnico).delete()
        db.commit()
        return True

    except Exception:
        db.rollback()
        return False
