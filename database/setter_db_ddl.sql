---------------------
-- Create database --
---------------------
CREATE DATABASE IF NOT EXISTS setter-db;
USE setter-db;

-----------------------
-- Tables definition --
-----------------------
-- Pessoas 
CREATE TABLE PESSOA (
    nome            VARCHAR(80) NOT NULL,
    cpf             VARCHAR(20) NOT NULL,
    rg              VARCHAR(20) NOT NULL,
    email           VARCHAR(80) NOT NULL,
    id              UUID NOT NULL,
    ddd             VARCHAR(5),
    numero          VARCHAR(20),
    data_nascimento TIMESTAMP NOT NULL,

    CONSTRAINT PESSOA_PK PRIMARY KEY (id)
);

CREATE TABLE ADMINISTRADOR (
    id              UUID NOT NULL,
    nome_usuario    VARCHAR(80) NOT NULL,
    senha           VARCHAR(80) NOT NULL,

    CONSTRAINT ADMINISTRADOR_UK UNIQUE (id),
    CONSTRAINT ADMINISTRADOR_PESSOA_FK FOREIGN KEY (id)
        REFERENCES PESSOA (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE ATLETA (
    id              UUID NOT NULL,

    CONSTRAINT ATLETA_UK UNIQUE (id),
    CONSTRAINT ATLETA_PESSOA_FK FOREIGN KEY (id)
        REFERENCES PESSOA (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

CREATE TABLE TREINADOR (
    id              UUID NOT NULL,
    cref            VARCHAR(30) NOT NULL,
    
    CONSTRAINT TREINADOR_UK UNIQUE (id),
    CONSTRAINT TREINADOR_PESSOA_FK FOREIGN KEY (id)
        REFERENCES PESSOA (id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
