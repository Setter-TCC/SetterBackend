from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Time
from src.schemas.time import TimeSchema
from src.utils.enums import NaipeTime


def create_time(db: Session, time: TimeSchema):
    try:
        _time = Time(id=time.id, nome=time.nome,
                     naipe=NaipeTime(time.naipe),
                     cnpj=time.cnpj, email=time.email)
        db.add(_time)
        db.commit()
        db.refresh(_time)
        return True

    except Exception:
        db.rollback()
        return False


def get_times(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Time).offset(skip).limit(limit).all()
        return query

    except Exception:
        db.rollback()
        return False


def get_time_by_id(db: Session, time_id: UUID):
    try:
        query = db.query(Time).Filter(Time.id == time_id).first()
        return query

    except Exception:
        db.rollback()
        return False


def update_time(db: Session, time_id: UUID):
    try:
        query = db.query(Time).Filter(Time.id == time_id)
        # Update da query pra cada campo passado
        db.commit()
        return True

    except Exception:
        db.rollback()
        return False


def delete_time(db: Session, time_id: UUID):
    try:
        db.query(Time).filter(Time.id == time_id).delete()
        db.commit()
        return True

    except Exception:
        db.rollback()
        return False
