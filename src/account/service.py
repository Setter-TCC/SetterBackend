from sqlalchemy.orm import Session
from src.models import Pessoa, Administrador, Atleta, Treinador
from src.schemas import Pessoa as PessoaSchema
from src.schemas import Administrador as AdministradorSchema
from src.schemas import Atleta as AtletaSchema
from src.schemas import Treinador as TreinadorSchema


def get_pessoas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pessoa).offset(skip).limit(limit).all()


def create_pessoa(db: Session, pessoa: PessoaSchema):
    _pessoa = Pessoa(nome=pessoa.nome, email=pessoa.email, cpf=pessoa.cpf,
                     rg=pessoa.rg, data_nascimento=pessoa.data_nascimento,
                     ddd=pessoa.ddd, numero=pessoa.numero, id=pessoa.id
                     )
    db.add(_pessoa)
    db.commit()
    db.refresh(_pessoa)

    return _pessoa


def get_atletas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pessoa, Atleta).join(Pessoa.id). \
        offset(skip).limit(limit).all()


def get_administradores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Pessoa, Administrador).join(Administrador.id). \
        offset(skip).limit(limit).all()
