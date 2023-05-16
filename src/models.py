from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from src.database import Base


class Pessoa(Base):
    __tablename__ = "pessoa"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    rg = Column(String, nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    ddd = Column(String, nullable=True)
    numero = Column(String, nullable=True)


class Administrador(Base):
    __tablename__ = "administrador"

    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True, nullable=False, unique=True)
    nome_usuario = Column(String, nullable=False)
    senha = Column(String, nullable=False)

    pessoa = relationship("Pessoa")


class Atleta(Base):
    __tablename__ = "atleta"

    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True, nullable=False, unique=True)

    pessoa = relationship("Pessoa")


class Treinador(Base):
    __tablename__ = "treinador"

    id = Column(Integer, ForeignKey("pessoa.id"), primary_key=True, nullable=False, unique=True)
    cref = Column(String, nullable=False)

    pessoa = relationship("Pessoa")


class Equipe(Base):
    __tablename__ = "equipe"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    estado = Column(String, nullable=False)
    cidade = Column(String, nullable=True)
    cnpj = Column(String, nullable=True)


class IntegracaoIntegra(Base):
    __tablename__ = "integracao_integra"

    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=True)
    ativo = Column(Boolean, nullable=False, default=True)
    tipo_pessoa = Column(String, nullable=False)
    equipe_id = Column(Integer, ForeignKey("equipe.id"))
    pessoa_id = Column(Integer, ForeignKey("pessoa.id"))
