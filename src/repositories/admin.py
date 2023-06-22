from uuid import UUID

from sqlalchemy.orm import Session

from src.models import Administrador
from src.schemas.administrador import AdministradorSchema


def create_admin(db: Session, admin: AdministradorSchema):
    try:
        _admin = Administrador(
            id=admin.id,
            nome_usuario=admin.nome_usuario,
            senha=admin.senha
        )
        db.add(_admin)
        db.commit()
        db.refresh(_admin)

        return True

    except Exception:
        return False


def get_all_admins(db: Session, skip: int = 0, limit: int = 100):
    try:
        query = db.query(Administrador).offset(skip).limit(limit).all()
        return query

    except Exception:
        return False


def get_admin_by_id(db: Session, id_admin: UUID):
    try:
        query = db.query(Administrador).filter_by(id=id_admin).first()
        return query

    except Exception:
        return False


def get_admin_by_nome_usuario(db: Session, nome_usuario: str):
    try:
        query = db.query(Administrador).filter_by(nome_usuario=nome_usuario).first()
        return query

    except Exception:
        return None


def update_admin(db: Session, admin: AdministradorSchema):
    try:
        query = db.query(Administrador).filter_by(id=admin.id).update({
            "senha": admin.senha
        })
        db.commit()
        return query

    except Exception:
        return False


def delete_admin(db: Session, admin_id: UUID):
    try:
        db.query(Administrador).filter_by(id=admin_id).delete()
        db.commit()
        return True

    except Exception:
        return False
