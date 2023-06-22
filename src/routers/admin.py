from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse

from src.configs.database import get_db
from src.internal.validators import token_validator
from src.repositories import admin_repository, pessoa_repository
from src.schemas import AdministradorUpdate, PessoaSchema, AdministradorSchema
from src.utils.crypt import crypt_context

admin_router = APIRouter(prefix="/admin", dependencies=[Depends(token_validator)])


@admin_router.get("", tags=["Admin"])
async def get_admin_data(db: Session = Depends(get_db), token: dict = Depends(token_validator)):
    username = token.get("sub")
    admin = admin_repository.get_admin_by_nome_usuario(db=db, nome_usuario=username)
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found."
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Success fetching admin.",
            "value": {
                "id": str(admin.id),
                "nome": admin.pessoa.nome,
                "email": admin.pessoa.email,
                "data_nascimento": admin.pessoa.data_nascimento.strftime(
                    "%d/%m/%Y") if admin.pessoa.data_nascimento else None,
                "cpf": admin.pessoa.cpf,
                "rg": admin.pessoa.rg,
                "telefone": admin.pessoa.telefone,
                "nome_usuario": admin.nome_usuario
            }
        }
    )


@admin_router.put("/update", tags=["Admin"])
async def update_admin(request: AdministradorUpdate, db: Session = Depends(get_db),
                       token: dict = Depends(token_validator)):
    if not request.id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Request body is not well formated."
        )

    username = token.get("sub")
    admin_on_db = admin_repository.get_admin_by_id(db=db, id_admin=request.id)

    if not admin_on_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found."
        )

    if admin_on_db.nome_usuario != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to update this admin."
        )

    if request.senha and request.nova_senha:
        if not crypt_context.verify(request.senha, admin_on_db.senha):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password."
            )

    pessoa = PessoaSchema(
        id=request.id,
        nome=request.nome,
        email=request.email,
        cpf=request.cpf,
        rg=request.rg,
        data_nascimento=request.data_nascimento,
        telefone=request.telefone
    )

    pessoa_ok = pessoa_repository.update_pessoa(db=db, pessoa=pessoa)
    if not pessoa_ok:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Could not update personal data for admin."
        )

    if request.senha and request.nova_senha:
        admin = AdministradorSchema(
            id=request.id,
            nome=request.nome,
            email=request.email,
            nome_usuario=request.nome_usuario,
            senha=crypt_context.hash(request.nova_senha)
        )
        admin_ok = admin_repository.update_admin(db=db, admin=admin)
        if not admin_ok:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail="Could not update account data for admin."
            )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "msg": "Updated admin succesfully."
        }
    )
